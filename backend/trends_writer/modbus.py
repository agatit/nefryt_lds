import asyncio
import logging
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer
from .config import Settings
from .plant import PipePlant


class PipePlantDataBlock(ModbusSequentialDataBlock):
    def __init__(self, address: int, values: list, pipe_plant: PipePlant):
        super().__init__(address, values)
        self.pipe_plant = pipe_plant

    def setValues(self, address, values):
        # logging.info(f"setValues: address={address}, relative = {address - self.address}, values={values}")
        try:
            self.pipe_plant.update(address - self.address, values)
            super().setValues(address, values)
        except Exception as e:
            logging.warning("setValues exception: " + str(e))

    def getValues(self, address, count=1):
        logging.info(f"getValues: address={address}, relative = {address - self.address}, count={count}")
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
        await StartAsyncTcpServer(
            context=server_context,
            address=('', port if port else Settings.modbus_port),
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        logging.info("Modbus server stopped")
