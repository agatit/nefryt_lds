import atexit
import logging
import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from config import Config, Settings
from database import lds
from db import get_engine
from simulator.simulations import SimulationDensityRKVolume, SimulationDensityPCHIPVolume, SimulationDensityRKMass, \
    SimulationDensityPCHIPMass

SIMULATION_CLASSES = {
    'DENSITY_VOLUME_RK': SimulationDensityRKVolume,
    'DENSITY_VOLUME_PCHIP': SimulationDensityPCHIPVolume,
    'DENSITY_MASS_RK': SimulationDensityRKMass,
    'DENSITY_MASS_PCHIP': SimulationDensityPCHIPMass
}

logger = logging.getLogger(__name__)


class SimulationManager:
    def __init__(self):
        self.simulations = []
        atexit.register(self.shutdown_processes)

    async def start_simulations(self):
        statement = (select(lds.Simulation)
                     .where(lds.Simulation.Enabled == 1)) # noqa
        logger.info("SimulationManager: Started reading simulations")
        with Session(get_engine()) as session:
            simulations = session.scalars(statement).all()

        for simulation in simulations:
            try:
                simulation_class = SIMULATION_CLASSES[simulation.SimulationDefID.strip()]
                new_simulation = simulation_class(simulation, Settings.TEST_DB_URI if Config.tests else Settings.DB_URI)
                self.simulations.append(new_simulation)
            except Exception as e:
                logger.warning(f"SimulationManager: Simulation with id = {simulation.ID} init error: {e}", exc_info=True)

        for simulation in self.simulations:
            simulation.run_process()
        logger.info("SimulationManager: Finished reading simulations")

        if Config.tests:
            return self.simulations
        else:
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("SimulationManager: Simulator module shutdown")
            return None

    def shutdown_processes(self):
        for simulation in self.simulations:
            simulation.process.terminate()
            simulation.process.join(1)
