import asyncio
import logging
from . import modbus
from . import plant


if __name__ == '__main__':
    logging.info('Server started\n')
    asyncio.run(modbus.run_server(plant.PipePlant()))
