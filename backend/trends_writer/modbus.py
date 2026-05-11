import asyncio
import logging
from typing import Any

from pymodbus.datastore import ModbusSequentialDataBlock, ModbusServerContext, ModbusDeviceContext
from pymodbus.server import StartAsyncTcpServer
from pymodbus.simulator import SimDevice, SimData, DataType
from pymodbus.simulator.simcore import SimCore

from .config import TrendsWriterSettings
from .plant import PipePlant

logger = logging.getLogger(__name__)


async def run_server(pipe_plant: PipePlant, port: int | None = None):
    async def on_register_access(
            function_code: int,
            start_address: int,
            address: int,
            count: int,
            current_registers: list,
            set_values: list | None,
    ):
        if set_values is not None:
            try:
                pipe_plant.update(address, set_values)
                logger.debug(f"Modbus: setValues (address={address}, values={set_values})")
            except Exception as e:
                logger.exception(f"Modbus: Exception in setValues: {e}", exc_info=True)
        else:
            logger.debug(f"Modbus: getValues (address={address}, count={count})")

    device = SimDevice(
        id=0,
        simdata=SimData(
            address=0,
            count=65535,
            values=0,
            datatype=DataType.REGISTERS,
        ),
        action=on_register_access,
    )

    try:
        logger.info(f"Modbus: Server started")
        await StartAsyncTcpServer(
            context=device,
            address=('', port if port else TrendsWriterSettings.modbus_port),
        )
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Modbus: Server stopped")
