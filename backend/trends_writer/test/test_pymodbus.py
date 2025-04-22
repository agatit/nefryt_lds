import asyncio
import math
import time
from unittest.mock import Mock
import pytest
from pymodbus.client import AsyncModbusTcpClient
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # noqa: E402
from trends_writer.modbus import run_server


@pytest.mark.asyncio
async def test_mocked_client_server_interaction():
    port = 5020
    mock_plant = Mock()
    server_task = asyncio.create_task(run_server(mock_plant, port))
    await asyncio.sleep(0.5)

    client = AsyncModbusTcpClient('localhost', port=port)
    await client.connect()
    res = await client.write_registers(0, [10, 20, 30])

    assert res.isError() is False
    mock_plant.update.assert_called_once()

    client.close()
    server_task.cancel()


async def _send_data(port: int, addr: int, data: list[int]):
    client = AsyncModbusTcpClient('localhost', port=port)
    await client.connect()
    res = await client.write_registers(addr, data)
    assert res.isError() is False
    client.close()


@pytest.mark.asyncio
async def test_mocked_server_client_interaction_when_multiple_calls():
    port = 5021
    mock_plant = Mock()
    server_task = asyncio.create_task(run_server(mock_plant, port))
    await asyncio.sleep(0.5)

    calls = 5
    tasks = 1
    tasks_list = []
    t = math.floor(time.time()) + 0.5
    for i in range(calls):
        for j in range(tasks):
            tasks_list.append(asyncio.create_task(_send_data(port, (i*j+i)*100, [i, j])))

        time.sleep(t - time.time() + 1)
        t += 1

    await asyncio.gather(*tasks_list)
    await asyncio.sleep(0.5)

    assert mock_plant.update.call_count == calls*tasks
    server_task.cancel()
