import asyncio
import logging
from config import setup_engine
from simulator.simulation_manager import SimulationManager

if __name__ == '__main__':
    logging.info('Simulator module started')
    setup_engine()
    asyncio.run(SimulationManager().start_simulations())
