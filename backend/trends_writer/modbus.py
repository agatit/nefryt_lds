import asyncio
import logging
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer
from .config import Settings
from .plant import PipePlant


logger = logging.getLogger(__name__)


class PipePlantDataBlock(ModbusSequentialDataBlock):
    def __init__(self, address: int, values: list, pipe_plant: PipePlant):
        super().__init__(address, values)
        self.pipe_plant = pipe_plant

    def setValues(self, address, values):
        try:
            self.pipe_plant.update(address - self.address, values)
            super().setValues(address, values)
            logger.debug(f"Modbus: setValues (address={address}, values={values})")
        except Exception as e:
            logger.warning(f"Modbus: Exception in setValues: {e}", exc_info=True)

    def getValues(self, address, count=1):
        logger.debug(f"Modbus: getValues (address={address}, count={count})")
        return super().getValues(address - self.address, count)


async def run_server(pipe_plant: PipePlant, port: int | None = None):
    datablock = PipePlantDataBlock(1, [0] * 1000, pipe_plant)
    slave_context = ModbusSlaveContext(
        hr=datablock,
        di=ModbusSequentialDataBlock.create(),
        co=ModbusSequentialDataBlock.create(),
        ir=ModbusSequentialDataBlock.create()
    )
    server_context = ModbusServerContext(slaves=slave_context, single=True)
    try:
        logger.info(f"Modbus: Server started")
        await StartAsyncTcpServer(
            context=server_context,
            address=('', port if port else Settings.modbus_port),
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Modbus: Server stopped")
