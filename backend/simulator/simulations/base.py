import atexit
import logging
import threading
import time
from multiprocessing import Process
from matplotlib.animation import FuncAnimation
from sqlalchemy import select, and_, literal, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from database.models import lds
from db import get_engine
from simulator.config import setup_engine
from simulator.simulations.utils import SimulatorData
import matplotlib.pyplot as plt


class SimulationBase:
    def __init__(self, simulation: lds.Simulation, db_uri: str, plot_sim: bool = False):
        self.time_buffer = 1
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

        self.distances = self.calculate_distances()
        self.simulation_data: list[SimulatorData] = []
        self.db_uri = db_uri
        self.process = None
        self.plot_sim = plot_sim
        atexit.register(self._shutdown)

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
        with Session(get_engine()) as session:
            unit: lds.Unit | None = session.get(lds.Unit, self.simulation_trend.UnitID)
        return unit

    def run_process(self):
        self.process = Process(target=self.run_simulation, args=(self.db_uri, ))
        self.process.start()
        logging.info(f"{self.__class__.__name__} ({self.lds_simulation.ID}) started")
        
    def calculate_distances(self):
        return [distance for distance in range(0, self.pipeline_length, self.lds_simulation.ResolutionMeters)]

    def calculate_simulation_data_on_start(self, current_timestamp: int):
        raise NotImplementedError

    def calculate_simulation_data(self, current_timestamp: int):
        raise NotImplementedError

    def save_simulation_data(self, timestamp: int):
        if len(self.simulation_data) == 0:
            logging.warning(f'Empty simulation data for simulation with id={self.lds_simulation.ID}')
            return
        db_data = [lds.SimulationData(SimulationID=self.lds_simulation.ID, Time=timestamp, Distance=0, Data=self.simulation_data[0].Data)]
        if len(self.distances) >= 2:
            iter_distance = iter(self.distances[1:])
            distance = next(iter_distance)
            for sim_data1, sim_data2 in zip(self.simulation_data[:-1], self.simulation_data[1:]):
                while distance is not None and sim_data1.Distance <= distance < sim_data2.Distance:
                    sim_data_distance_diff = sim_data2.Distance - sim_data1.Distance
                    distance_diff1 = abs(sim_data1.Distance - distance)
                    distance_diff2 = abs(sim_data2.Distance - distance)
                    if sim_data1.Data is None and sim_data2.Data is None:
                        calculated_data = None
                    elif sim_data1.Data is None:
                        calculated_data = sim_data2.Data
                    elif sim_data2.Data is None:
                        calculated_data = sim_data1.Data
                    else:
                        calculated_data = ((((sim_data_distance_diff - distance_diff1) / sim_data_distance_diff) * sim_data1.Data)
                                           + (((sim_data_distance_diff - distance_diff2) / sim_data_distance_diff) * sim_data2.Data))
                    db_data.append(lds.SimulationData(SimulationID=self.lds_simulation.ID, Time=timestamp, Distance=distance, Data=calculated_data))
                    distance = next(iter_distance, None)

        with Session(get_engine()) as session:
            for lds_simulation_data in db_data:
                session.merge(lds_simulation_data)
                session.commit()

    def run_simulation(self, db_uri: str):
        setup_engine(db_uri)
        current_timestamp = int(time.time()) - self.time_buffer
        self.calculate_simulation_data_on_start(current_timestamp)
        if self.plot_sim:
            fig, ax = plt.subplots()

            def _update_simulation_plot(_):
                xs = [data.Distance for data in self.simulation_data]
                ys = [data.Data if data.Data is not None else 0 for data in self.simulation_data]

                ax.clear()
                ax.set_title(f'Simulation {self.lds_simulation.ID} in timestamp {int(time.time())}')
                ax.plot(xs, ys)
                fig.canvas.draw()

            threading.Thread(
                target=self._run_simulation_loop,
                args=(current_timestamp,),
                daemon=True
            ).start()

            anim = FuncAnimation(fig, _update_simulation_plot, cache_frame_data=False, interval=1000)  # noqa
            plt.show()
        else:
            self._run_simulation_loop(current_timestamp)

    def _run_simulation_loop(self, current_timestamp: int):
        simulation_time = 0
        while True:
            start_time = time.perf_counter()
            try:
                self.calculate_simulation_data(current_timestamp)
            except Exception as e:
                logging.warning(f"{self.__class__.__name__} ({self.lds_simulation.ID}) error while simulation data read: {e}")

            if simulation_time % self.lds_simulation.RefreshTimeSeconds == 0:
                self.save_simulation_data(current_timestamp)

            if 1 - (time.perf_counter() - start_time) > 0:
                time.sleep(1 - (time.perf_counter() - start_time))
            current_timestamp += 1

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
