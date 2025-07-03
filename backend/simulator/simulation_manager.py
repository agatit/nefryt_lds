import atexit
import logging
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import lds
from db import get_engine
from .config import Settings
from .simulations.density import create_simulation_density_object

SIMULATION_CLASSES = {
    'DENSITY': create_simulation_density_object,
}


class SimulationManager:
    def __init__(self):
        self.simulations = []
        self.start_simulations()
        atexit.register(self.shutdown_processes)

    def start_simulations(self):
        statement = select(lds.Simulation)
        with Session(get_engine()) as session:
            simulations = session.execute(statement).all()

        for simulation in simulations:
            try:
                simulation_class = SIMULATION_CLASSES[simulation.SimulationDefID.strip()]
                new_simulation = simulation_class(simulation.ID, Settings.db_uri)
                self.simulations.append(new_simulation)
            except Exception as e:
                logging.warning(f"Simulation with id = ({simulation.ID}) init error: {e}", exc_info=True)

        for simulation in simulations:
            simulation.run_process()

    def shutdown_processes(self):
        for simulation in self.simulations:
            simulation.process.terminate()
            simulation.process.join(1)
