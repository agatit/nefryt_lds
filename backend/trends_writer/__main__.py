import asyncio
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import setup_engine
from trends_writer.profiler import Profiler
from . import modbus
from . import plant

if __name__ == '__main__':
    setup_engine()
    Profiler.init()
    asyncio.run(modbus.run_server(plant.PipePlant()))
