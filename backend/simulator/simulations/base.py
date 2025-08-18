import atexit
import logging
import math
import time
from multiprocessing import Process
import numpy as np
from sqlalchemy import select, and_, literal, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from config import setup_engine, Settings
from database.models import lds
from db import get_engine

# TODO: skrypt do prezentacji danych symulacji


class SimulationBase:
    def __init__(self, simulation: lds.Simulation, db_uri: str = None):
        self.lds_simulation = simulation
        self._read_params()
        try:
            self.pipeline_length = int(self.params['LENGTH'])
        except KeyError:
            raise ValueError(f'No \'LENGTH\' param for simulation {self.lds_simulation.ID}')
        except ValueError:
            raise ValueError(f'\'LENGTH\' param for simulation {self.lds_simulation.ID} must be an integer')

        self.simulation_trend = self._read_trend()
        if self.simulation_trend is None:
            raise ValueError(f'No trend with id={self.lds_simulation.TrendID} for simulation with id={self.lds_simulation.ID}')

        self.simulation_unit = self._read_unit()
        if self.simulation_unit is None:
            raise ValueError(f'No unit with id = {self.simulation_trend.UnitID} for trend with id = {self.lds_simulation.TrendID} '
                                 f'for simulation {self.lds_simulation.ID}')

        try:
           flow_trend_id = self.params['FLOW_TREND']
        except KeyError:
            raise ValueError(f'No param \'FLOW_TREND\' for simulation {self.lds_simulation.ID}')

        self._read_flow_trend(flow_trend_id)
        if self.flow_trend is None:
            raise ValueError(f'No flow trend with id = {flow_trend_id} for simulation {self.lds_simulation.ID}')

        self.time_buffer = self.calculate_time_buffer()
        self.simulation_timestamp = int(time.time()) - self.time_buffer
        self.last_success = self.simulation_timestamp - 1
        self.distances = self.calculate_distances()
        segments_number = math.ceil(self.pipeline_length / self.lds_simulation.ResolutionMeters) \
            if math.ceil(self.pipeline_length / self.lds_simulation.ResolutionMeters) > 200 \
            else (200 if self.pipeline_length > 200 else self.pipeline_length)
        self.simulation_segment_length = self.pipeline_length / segments_number
        self.simulation_data: np.ndarray = np.zeros(segments_number)
        self.simulation_data_gradient: np.ndarray = np.zeros(segments_number)
        self.db_uri = db_uri
        if self.db_uri:
            self.save_simulation_data()
        self.process = None
        atexit.register(self._shutdown)

        # self.pipe_volume = self.pipe_area * self.segments_length


    def _read_params(self):
        statement = (select(lds.SimulationParamDef, lds.SimulationParam)
                .select_from(lds.Simulation)
                .join(lds.SimulationDef, lds.Simulation.SimulationDefID == lds.SimulationDef.ID) # noqa
                .join(lds.SimulationParamDef, lds.SimulationDef.ID == lds.SimulationParamDef.SimulationDefID)
                .join(lds.SimulationParam, and_(lds.SimulationParamDef.ID == lds.SimulationParam.SimulationParamDefID, lds.Simulation.ID == lds.SimulationParam.SimulationID))
                .where(lds.Simulation.ID == literal(self.lds_simulation.ID)))

        with Session(get_engine()) as session:
            read_params = session.execute(statement).fetchall()
        self.params = {}
        for simulation_param_def, simulation_param in read_params:
            self.params[simulation_param_def.ID.strip()] = simulation_param.Value

    def _read_trend(self):
        with Session(get_engine()) as session:
            lds_trend = session.get(lds.Trend, self.lds_simulation.TrendID)
        return lds_trend

    def _read_unit(self):
        if self.simulation_trend.UnitID is None:
            return None
        with Session(get_engine()) as session:
            unit: lds.Unit | None = session.get(lds.Unit, self.simulation_trend.UnitID)
        return unit

    def _read_flow_trend(self, flow_trend_id: int):
        with Session(get_engine()) as session:
            lds_trend = session.get(lds.Trend, flow_trend_id)
        self.flow_trend = lds_trend

    def run_process(self):
        self.process = Process(target=self.run_simulation, args=(self.db_uri, ))
        self.process.start()
        logging.info(f"{self.__class__.__name__} ({self.lds_simulation.ID}) started")

    def calculate_time_buffer(self):
        return max(self.simulation_trend.TimeDelta, self.flow_trend.TimeDelta) + 3
        
    def calculate_distances(self):
        return [distance for distance in range(0, self.pipeline_length, self.lds_simulation.ResolutionMeters)]

    def calculate_simulation_data_on_start(self):
        raise NotImplementedError

    def calculate_simulation_data(self):
        raise NotImplementedError

    def save_simulation_data(self):
        print('saving simulation')
        # print(time.time())
        # print(self.simulation_data)
        if len(self.simulation_data) == 0:
            logging.warning(f'Empty simulation data for simulation with id={self.lds_simulation.ID}')
            return
        db_data = [lds.SimulationData(SimulationID=self.lds_simulation.ID, Time=self.simulation_timestamp,
                                      Distance=0, Data=np.round(self.simulation_data[0]))]
        # print(self.distances)
        if len(self.distances) >= 2:
            iter_distance = iter(self.distances[1:])
            distance = next(iter_distance)
            while distance is not None:
                # print(distance)
                # print('==============')
                # print(distance)
                # print(self.simulation_segment_length)
                idx = int(distance // self.simulation_segment_length)
                # print(idx)
                sim_data1 = self.simulation_data[idx]
                sim_data2 = self.simulation_data[idx + 1]
                # print(sim_data1)
                # print(sim_data2)
                distance_diff1 = abs(idx*self.simulation_segment_length - distance)
                distance_diff2 = abs((idx+1)*self.simulation_segment_length - distance)
                # print(distance_diff1)
                # print(distance_diff2)
                if sim_data1 is None and sim_data2 is None:
                    calculated_data = None
                elif sim_data1 is None:
                    calculated_data = sim_data2
                elif sim_data2 is None:
                    calculated_data = sim_data1
                else:
                    calculated_data = ((((self.simulation_segment_length - distance_diff1) / self.simulation_segment_length) * sim_data1)
                                       + (((self.simulation_segment_length - distance_diff2) / self.simulation_segment_length) * sim_data2))
                db_data.append(lds.SimulationData(SimulationID=self.lds_simulation.ID, Time=self.simulation_timestamp,
                                                  Distance=distance, Data=calculated_data))
                # print(calculated_data)
                distance = next(iter_distance, None)

        with Session(get_engine()) as session:
            for lds_simulation_data in db_data:
                session.merge(lds_simulation_data)
                session.commit()

    def run_simulation(self, db_uri: str):
        setup_engine(db_uri)
        self.calculate_simulation_data_on_start()
        self._run_simulation_loop()
        # if self.plot_sim:
        #     fig, ax = plt.subplots()
        #
        #     def _update_simulation_plot(_):
        #         xs = [data.Distance for data in self.simulation_data]
        #         ys = [data.Data if data.Data is not None else 0 for data in self.simulation_data]
        #
        #         ax.clear()
        #         ax.set_title(f'Simulation {self.lds_simulation.ID} in timestamp {int(time.time())}')
        #         ax.plot(xs, ys)
        #         fig.canvas.draw()
        #
        #     threading.Thread(
        #         target=self._run_simulation_loop,
        #         args=(current_timestamp,),
        #         daemon=True
        #     ).start()
        #
        #     anim = FuncAnimation(fig, _update_simulation_plot, cache_frame_data=False, interval=1000)  # noqa
        #     plt.show()
        # else:
        # self._run_simulation_loop(current_timestamp)

    def _run_simulation_loop(self):
        simulation_length = 1
        try:
            while True:
                start_time = time.perf_counter()
                try:
                    self.calculate_simulation_data()
                except Exception as e:
                    logging.warning(f"{self.__class__.__name__} ({self.lds_simulation.ID}) error while simulation data read: {e}")

                if simulation_length % self.lds_simulation.RefreshTimeSeconds == 0:
                    self.save_simulation_data()

                if 1 - (time.perf_counter() - start_time) > 0:
                    time.sleep(1 - (time.perf_counter() - start_time))
                simulation_length += 1
                self.simulation_timestamp += 1
        except KeyboardInterrupt:
            logging.info(f"{self.__class__.__name__} ({self.lds_simulation.ID}) closed")

    def _delete_data_from_db(self):
        try:
            statement = delete(lds.SimulationData).where(lds.SimulationData.SimulationID == self.lds_simulation.ID) # noqa
            with Session(get_engine()) as session:
                session.execute(statement)
                session.commit()
        except SQLAlchemyError:
            pass

    def _shutdown(self):
        self._delete_data_from_db()
        if self.process:
            self.process.terminate()
            self.process.join()
