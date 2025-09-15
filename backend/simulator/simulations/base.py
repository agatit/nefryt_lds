import atexit
import logging
import math
import threading
import time
from multiprocessing import Process
from multiprocessing.connection import Listener
import numpy as np
from sqlalchemy import select, and_, literal, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config import setup_engine
from database.models import lds
from db import get_engine
from simulator.config import SimulatorSettings

logger = logging.getLogger(__name__)


class SimulationBase:
    def __init__(self, simulation: lds.Simulation, db_uri: str = None):
        self.lds_simulation = simulation
        self.id = self.lds_simulation.ID
        self._read_params()
        try:
            self.pipeline_length = int(self.params['LENGTH'])
        except KeyError:
            raise ValueError(f'No \'LENGTH\' param in simulation with id={self.id}')
        except ValueError:
            raise ValueError(f'\'LENGTH\' param in simulation with id={self.id} has to be an integer')

        self.simulation_trend = self._read_trend(self.lds_simulation.TrendID)
        if self.simulation_trend is None:
            raise ValueError(f'No trend with id={self.lds_simulation.TrendID} in simulation with id={self.id}')

        self.simulation_unit = self._read_unit(self.simulation_trend.UnitID)
        if self.simulation_unit is None:
            raise ValueError(f'No unit with id={self.simulation_trend.UnitID} for trend with id={self.lds_simulation.TrendID} '
                                 f'in simulation with id={self.id}')

        try:
           flow_trend_id = self.params['FLOW_TREND_ID']
        except KeyError:
            raise ValueError(f'No param \'FLOW_TREND_ID\' for simulation with id={self.id}')

        self.flow_trend = self._read_trend(flow_trend_id)
        if self.flow_trend is None:
            raise ValueError(f'No flow trend with id={flow_trend_id} for simulation with id={self.id}')

        self.flow_unit = self._read_unit(self.flow_trend.UnitID)
        if self.flow_unit is None:
            raise ValueError(
                f'No unit with id={self.flow_trend.UnitIDD} for flow trend with id={flow_trend_id} '
                f'for simulation with id={self.id}')

        self.time_buffer = self.calculate_time_buffer()
        self.simulation_timestamp = int(time.time()) - self.time_buffer
        self.distances = self.calculate_distances()
        segments_number = math.ceil(self.pipeline_length / self.lds_simulation.ResolutionMeters) \
            if math.ceil(self.pipeline_length / self.lds_simulation.ResolutionMeters) > 1000 else 1000
        self.simulation_segment_length = self.pipeline_length / segments_number
        self.simulation_data: np.ndarray = np.zeros(segments_number)
        self.simulation_data_gradient: np.ndarray = np.zeros(segments_number)
        self.db_uri = db_uri
        if self.db_uri:
            self.save_simulation_data()
        self.previous_timestamp_diff = 0
        self.process = None
        self.displayer_listener = None
        self.displayer_connection = None
        atexit.register(self._shutdown)
        logger.info(f"{self.__class__.__name__} ({self.id}): Simulation initialized (params={self.params})")

    def _read_params(self):
        statement = (select(lds.SimulationParamDef, lds.SimulationParam)
                .select_from(lds.Simulation)
                .join(lds.SimulationDef, lds.Simulation.SimulationDefID == lds.SimulationDef.ID) # noqa
                .join(lds.SimulationParamDef, lds.SimulationDef.ID == lds.SimulationParamDef.SimulationDefID)
                .join(lds.SimulationParam, and_(lds.SimulationParamDef.ID == lds.SimulationParam.SimulationParamDefID, lds.Simulation.ID == lds.SimulationParam.SimulationID))
                .where(lds.Simulation.ID == literal(self.id)))

        with Session(get_engine()) as session:
            read_params = session.execute(statement).fetchall()
        self.params = {}
        for simulation_param_def, simulation_param in read_params:
            self.params[simulation_param_def.ID.strip()] = simulation_param.Value

    @staticmethod
    def _read_trend(trend_id: int):
        with Session(get_engine()) as session:
            lds_trend = session.get(lds.Trend, trend_id)
        return lds_trend

    @staticmethod
    def _read_unit(unit_id: str):
        with Session(get_engine()) as session:
            unit: lds.Unit | None = session.get(lds.Unit, unit_id)
        return unit

    def run_process(self):
        self.process = Process(target=self.run_simulation, args=(self.db_uri, ))
        self.process.start()
        logger.info(f"{self.__class__.__name__} ({self.id}): Process started")

    def calculate_time_buffer(self):
        return max(self.simulation_trend.TimeDelta, self.flow_trend.TimeDelta) + 3
        
    def calculate_distances(self):
        return [distance for distance in range(0, self.pipeline_length, self.lds_simulation.ResolutionMeters)]

    def calculate_simulation_data_on_start(self):
        raise NotImplementedError

    def calculate_simulation_data(self):
        raise NotImplementedError

    def save_simulation_data(self):
        if len(self.simulation_data) == 0:
            logger.warning(f'{self.__class__.__name__} ({self.id}): Empty simulation data')
            return
        db_data = [lds.SimulationData(SimulationID=self.id, Time=self.simulation_timestamp,
                                      Distance=0, Data=np.round(self.simulation_data[0]))]
        if len(self.distances) >= 2:
            iter_distance = iter(self.distances[1:])
            distance = next(iter_distance)
            while distance is not None:
                idx = int(distance // self.simulation_segment_length)
                sim_data1 = self.simulation_data[idx]
                sim_data2 = self.simulation_data[idx + 1]
                distance_diff1 = abs(idx*self.simulation_segment_length - distance)
                distance_diff2 = abs((idx+1)*self.simulation_segment_length - distance)
                if sim_data1 is None and sim_data2 is None:
                    calculated_data = None
                elif sim_data1 is None:
                    calculated_data = sim_data2
                elif sim_data2 is None:
                    calculated_data = sim_data1
                else:
                    calculated_data = ((((self.simulation_segment_length - distance_diff1) / self.simulation_segment_length) * sim_data1)
                                       + (((self.simulation_segment_length - distance_diff2) / self.simulation_segment_length) * sim_data2))
                db_data.append(lds.SimulationData(SimulationID=self.id, Time=self.simulation_timestamp,
                                                  Distance=distance, Data=calculated_data))
                distance = next(iter_distance, None)

        with Session(get_engine()) as session:
            for lds_simulation_data in db_data:
                session.merge(lds_simulation_data)
                session.commit()
        logger.debug(f'{self.__class__.__name__} ({self.id}): Saved simulation data: ({db_data})')

    def run_simulation(self, db_uri: str):
        setup_engine(db_uri)
        self.simulation_timestamp = int(time.time()) - self.time_buffer
        self._check_timestamp_compatibility()
        if SimulatorSettings.displayer_ports and self.id in SimulatorSettings.displayer_ports.keys():
            threading.Thread(target=self._run_simulation_data_sender, daemon=True).start()
        self.calculate_simulation_data_on_start()
        self.save_simulation_data()
        self._run_simulation_loop()

    def _check_timestamp_compatibility(self):
        statement = (select(lds.TrendData)
                     .where(lds.TrendData.TrendID == self.flow_trend.ID) # noqa
                     .where(lds.TrendData.Time > self.simulation_timestamp)
                     .limit(1))

        with Session(get_engine()) as session:
            data = session.execute(statement).scalars().first()

        if data is not None and data.Time > int(time.time()) + 1:
            logger.warning(f'{self.__class__.__name__} ({self.id}): Timestamp gap between Trends Writer and Simulation modules'
                            f'(current gap: {data.Time - int(time.time())} seconds). '
                            f'Simulator may not calculate and save most recent data')
    def _run_simulation_loop(self):
        simulation_duration = 1
        try:
            while True:
                start_time = time.perf_counter()
                try:
                    self.calculate_simulation_data()
                except Exception as e:
                    logger.warning(f"{self.__class__.__name__} ({self.id}): Error while simulation data read: {e}", exc_info=True)

                if simulation_duration % self.lds_simulation.RefreshTimeSeconds == 0:
                    self.save_simulation_data()

                if 1 - (time.perf_counter() - start_time) > 0 and self.simulation_timestamp >= time.time() - self.time_buffer:
                    time.sleep(1 - (time.perf_counter() - start_time))
                simulation_duration += 1
                self.simulation_timestamp += 1
        except KeyboardInterrupt:
            logger.info(f"{self.__class__.__name__} ({self.id}): Closing")

    def _run_simulation_data_sender(self):
        logger.debug(f"{self.__class__.__name__} ({self.id}): Simulation data sender started")
        self.displayer_listener = Listener(('localhost', SimulatorSettings.displayer_ports[self.id]),
                                           authkey=b'secret')
        while True:
            if not self.displayer_connection:
                self.displayer_connection = self.displayer_listener.accept()
                logger.debug(f"{self.__class__.__name__} ({self.id}): Displayer connection established")
            try:
                self.displayer_connection.send((self.pipeline_length, self.simulation_data))
            except (BrokenPipeError, ConnectionResetError, EOFError):
                logger.debug(f"{self.__class__.__name__} ({self.id}): Displayer connection closed")
                self.displayer_connection.close()
                self.displayer_connection = None
            finally:
                logger.debug(f"{self.__class__.__name__} ({self.id}): Simulation data sender closed")
                time.sleep(1)

    def _delete_data_from_db(self):
        try:
            statement = delete(lds.SimulationData).where(lds.SimulationData.SimulationID == self.id) # noqa
            with Session(get_engine()) as session:
                session.execute(statement)
                session.commit()
        except SQLAlchemyError:
            pass

    def _shutdown(self):
        self._delete_data_from_db()
        if self.displayer_connection:
            self.displayer_connection.close()
        if self.displayer_listener:
            self.displayer_listener.close()
        if self.process:
            self.process.terminate()
            self.process.join()
