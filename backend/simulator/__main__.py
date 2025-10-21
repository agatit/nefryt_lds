import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import setup_engine
from simulator.simulation_manager import SimulationManager

if __name__ == '__main__':
    setup_engine()
    asyncio.run(SimulationManager().start_simulations())
