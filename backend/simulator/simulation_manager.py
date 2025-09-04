import atexit
import logging
import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from config import Settings
from database import lds
from db import get_engine
from .simulations.density_mass import SimulationDensityMass
from .simulations.density_volume import SimulationDensityVolume

SIMULATION_CLASSES = {
    'DENSITY_VOLUME': SimulationDensityVolume,
    'DENSITY_MASS': SimulationDensityMass,
}


class SimulationManager:
    def __init__(self):
        self.simulations = []
        atexit.register(self.shutdown_processes)

    async def start_simulations(self):
        statement = select(lds.Simulation)
        with Session(get_engine()) as session:
            simulations = session.scalars(statement).all()

        for simulation in simulations:
            try:
                simulation_class = SIMULATION_CLASSES[simulation.SimulationDefID.strip()]
                new_simulation = simulation_class(simulation, Settings.db_uri)
                self.simulations.append(new_simulation)
            except Exception as e:
                logging.warning(f"Simulation with id = {simulation.ID} init error: {e}", exc_info=True)

        for simulation in self.simulations:
            simulation.run_process()

        if Settings.tests:
            return self.simulations
        else:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logging.info("Simulator module shutdown")
            return None

    def shutdown_processes(self):
        for simulation in self.simulations:
            simulation.process.terminate()
            simulation.process.join(1)
