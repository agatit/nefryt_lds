import logging
import time
from abc import ABC, abstractmethod
from multiprocessing import Process

from sqlalchemy import select, and_, literal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.models import lds
from db import get_engine
from simulator.config import setup_engine


class SimulationBase:
    def __init__(self, simulation: lds.Simulation, db_uri: str):
        self.id = simulation.ID
        self.simulation_trend_id = simulation.TrendID
        self.refresh_time = simulation.RefreshTimeSeconds
        self._read_params()
        self.simulation_resolution = simulation.ResolutionMeters
        try:
            self.simulation_length = self.params['LENGTH']
        except KeyError:
            raise ValueError(f'No \'LENGTH\' param for simulation {self.id}')
        self.distances = self.calculate_distances()
        self.db_uri = db_uri
        self.process = None
        
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

    def run_process(self):
        self.process = Process(target=self.run_simulation, args=(self.db_uri, ))
        self.process.start()
        logging.info(f"{self.__class__.__name__} ({self.id}) started")
        
    def calculate_distances(self):
        return [distance for distance in range(0, self.simulation_length, self.simulation_resolution)]

    def calculate_simulation_data(self):
        raise NotImplementedError

    def save_simulation_data(self):
        pass

    def run_simulation(self, db_uri: str):
        setup_engine(db_uri)

        while True:
            start_time = time.perf_counter()
            try:
                data = self.calculate_simulation_data()
                self.save_simulation_data()
            except Exception as e:
                logging.warning(f"{self.__class__.__name__} ({self.id}) error while simulation data read: {e}")
            finally:
                time.sleep(self.refresh_time - (time.perf_counter() - start_time))
