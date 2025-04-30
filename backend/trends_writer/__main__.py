import asyncio
import logging
from multiprocessing.pool import Pool
from trends_writer.profiler import Profiler
from . import modbus
from . import plant


if __name__ == '__main__':
    logging.info('Server started\n')

    use_asyncio = True
    Profiler.init(use_asyncio)
    asyncio.run(modbus.run_server(plant.PipePlant(Pool(), use_asyncio=use_asyncio, use_profiler=True)))
