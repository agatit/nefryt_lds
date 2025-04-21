import logging
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server import StartAsyncTcpServer
from .config import config
from .plant import PipePlant


class PipePlantDataBlock(ModbusSequentialDataBlock):
    def __init__(self, address: int, values: list, pipe_plant: PipePlant):
        super().__init__(address, values)
        self.pipe_plant = pipe_plant

    def setValues(self, address, values):
        logging.info(f"setValues: address={address}, values={values}")
        self.pipe_plant.update(address, values)
        super().setValues(address, values)

    def getValues(self, address, count=1):
        logging.info("getValues: address={address}, count={count}")
        return super().getValues(address, count)


async def run_server(pipe_plant):
    datablock = PipePlantDataBlock(0, [0]*1000, pipe_plant)
    slave_context = ModbusSlaveContext(hr=datablock)
    server_context = ModbusServerContext(slaves=slave_context, single=True)

    await StartAsyncTcpServer(
        context=server_context,
        address=('', config.get("modbus_port", 502)),
    )
