import asyncio
import math
import struct
import time
from random import randint
from unittest.mock import patch
import pytest
from pymodbus.client import AsyncModbusTcpClient
import sys
import os
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from db import get_engine
from trends_writer.profiler import Profiler
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # noqa: E402
from database.models import lds
from trends_writer.plant import PipePlant
from trends_writer.modbus import run_server

trend_param1 = lds.TrendParam(TrendParamDefID='MODBUS_REGISTER', TrendID=1, Value='1000')
trend_param2 = lds.TrendParam(TrendParamDefID='FILTER_WINDOW', TrendID=2, Value='2')
trend_def1 = lds.TrendDef(ID='QUICK', Name='TrendDef1')
trend_def2 = lds.TrendDef(ID='DERIV', Name='TrendDef2')
trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
trend3 = lds.Trend(ID=3, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)

def add_two_objects():
    global trend_param1, trend1, trend_def1, trend3
    trend_def1 = lds.TrendDef(ID='QUICK', Name='TrendDef1')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend3 = lds.Trend(ID=3, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend_param1 = lds.TrendParam(TrendParamDefID='MODBUS_REGISTER', TrendID=1, Value='1000')
    trend_param3 = lds.TrendParam(TrendParamDefID='MODBUS_REGISTER', TrendID=3, Value='2000')
    trend_param_def = lds.TrendParamDef(ID='MODBUS_REGISTER', TrendDefID='QUICK', Name='name', DataType='INT')
    objs = [[trend_def1], [trend1, trend3], [trend_param1, trend_param3], [trend_param_def]]

    return objs


def add_objects():
    global trend_param1, trend1, trend_def1
    trend_def1 = lds.TrendDef(ID='QUICK', Name='TrendDef1')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend_param1 = lds.TrendParam(TrendParamDefID='MODBUS_REGISTER', TrendID=1, Value='1000')
    trend_param_def = lds.TrendParamDef(ID='MODBUS_REGISTER', TrendDefID='QUICK', Name='name', DataType='INT')
    objs = [[trend_def1], [trend1], [trend_param1], [trend_param_def]]

    return objs


def add_objects_with_children():
    global trend_param1, trend_param2, trend_def1, trend_def2, trend1, trend2
    trend_def1 = lds.TrendDef(ID='QUICK', Name='TrendDef1')
    trend_def2 = lds.TrendDef(ID='DERIV', Name='TrendDef2')
    trend1 = lds.Trend(ID=1, TrendDefID=trend_def1.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend2 = lds.Trend(ID=2, TrendDefID=trend_def2.ID, RawMin=1, RawMax=10, ScaledMin=0.5, ScaledMax=1.5)
    trend_param1 = lds.TrendParam(TrendParamDefID='MODBUS_REGISTER', TrendID=1, Value='1000')
    trend_param2 = lds.TrendParam(TrendParamDefID='FILTER_WINDOW', TrendID=2, Value='2')
    trend_param3 = lds.TrendParam(TrendParamDefID='TREND_ID', TrendID=2, Value='1')
    trend_param_def1 = lds.TrendParamDef(ID='MODBUS_REGISTER', TrendDefID='QUICK', Name='name', DataType='INT')
    trend_param_def2 = lds.TrendParamDef(ID='FILTER_WINDOW', TrendDefID='DERIV', Name='name', DataType='INT')
    trend_param_def3 = lds.TrendParamDef(ID='TREND_ID', TrendDefID='DERIV', Name='name', DataType='TREND')
    objs = [[trend_def1, trend_def2], [trend1, trend2],
            [trend_param1, trend_param2, trend_param3], [trend_param_def1, trend_param_def2, trend_param_def3]]

    return objs

def init_profiler(trend_ids: list):
    Profiler.init()
    Profiler.set_trends(trend_ids, [])


def _get_trend_data_records_count():
    with Session(get_engine()) as session:
        return session.execute(select(func.count()).select_from(lds.TrendData)).fetchall()[0][0]


def _get_profiler_data_active_trends_count():
    with Session(get_engine()) as session:
        return session.execute(select(func.count()).select_from(lds.ProfilerData)
                               .where(lds.ProfilerData.Time10 != None)).fetchall()[0][0] # noqa


def _get_trend_data_records():
    with Session(get_engine()) as session:
        return session.execute(select(lds.TrendData)).fetchall()


async def _send_data(port: int, addr: int, data: list[int]):
    client = AsyncModbusTcpClient('localhost', port=port)
    await client.connect()
    res = await client.write_registers(addr, data)
    assert res.isError() is False
    client.close()


@pytest.mark.asyncio
@pytest.mark.parametrize('reset_lds_objects', [add_objects], indirect=True)
async def test_trend_data_should_be_written_to_db_when_correct_address(add_lds_objects):
    port = 5022
    init_profiler([trend1.ID])
    server_task = asyncio.create_task(run_server(PipePlant(), port))
    await asyncio.sleep(0.5)
    calls = 2

    t = math.floor(time.time()) + 0.5
    for i in range(calls):
        await _send_data(port, int(trend_param1.Value),  [randint(0, 255) for _ in range(100)])
        await asyncio.sleep(t - time.time() + 1)
        t += 1

    server_task.cancel()

    assert _get_trend_data_records_count() == calls


@pytest.mark.asyncio
@pytest.mark.parametrize('reset_lds_objects', [add_objects], indirect=True)
async def test_trend_data_should_write_only_when_correct_address(add_lds_objects):
    port = 5023
    init_profiler([trend1.ID])
    server_task = asyncio.create_task(run_server(PipePlant(), port))
    await asyncio.sleep(0.5)
    calls = 2
    tasks = 3

    tasks_list = []
    t = math.floor(time.time()) + 0.5
    for i in range(calls):
        for j in range(tasks):
            tasks_list.append(asyncio.create_task(
                _send_data(port, int(trend_param1.Value) * j, [randint(0, 255) for _ in range(100)])))
        await asyncio.sleep(t - time.time() + 1)
        t += 1

    await asyncio.gather(*tasks_list)
    server_task.cancel()

    assert _get_trend_data_records_count() == calls


@pytest.mark.asyncio
@pytest.mark.parametrize('reset_lds_objects', [add_objects_with_children], indirect=True)
async def test_trend_data_should_write_trend_data_for_children_trends(add_lds_objects):
    port = 5024
    init_profiler([trend1.ID, trend2.ID])
    server_task = asyncio.create_task(run_server(PipePlant(), port))
    await asyncio.sleep(0.5)
    calls = 10

    t = math.floor(time.time()) + 0.5
    for i in range(calls):
        await _send_data(port, int(trend_param1.Value), [1 for _ in range(100)])
        await asyncio.sleep(t - time.time() + 1)
        t += 1

    server_task.cancel()

    assert calls < _get_trend_data_records_count() <= (2*calls - int(trend_param2.Value))


@pytest.mark.asyncio
@pytest.mark.parametrize('reset_lds_objects', [add_objects], indirect=True)
async def test_trend_data_should_not_update_data_when_the_same_primary_key_in_one_timestamp(add_lds_objects):
    port = 5025
    init_profiler([trend1.ID])
    server_task = asyncio.create_task(run_server(PipePlant(), port))
    await asyncio.sleep(0.5)
    calls = 2

    t_start = 100
    t = t_start
    for i in range(calls):
        with patch('trends_writer.plant.time') as mock_time:
            mock_time.time.return_value = t
            await _send_data(port, int(trend_param1.Value),  [i for _ in range(100)])
            await asyncio.sleep(1)

    server_task.cancel()

    trend_data = _get_trend_data_records()
    assert _get_trend_data_records_count() == 1
    data = trend_data[0][0].Data
    data = struct.unpack("H" * 100, data)
    assert all(val == 0 for val in data)


@pytest.mark.asyncio
@pytest.mark.parametrize('reset_lds_objects', [add_objects], indirect=True)
async def test_trend_data_should_update_data_when_the_same_primary_key_in_repeated_timestamp(add_lds_objects):
    port = 5026
    init_profiler([trend1.ID])
    server_task = asyncio.create_task(run_server(PipePlant(), port))
    await asyncio.sleep(0.5)
    calls = 3

    t_start = 100
    t = t_start
    for i in range(calls):
        with patch('trends_writer.plant.time') as mock_time:
            mock_time.time.return_value = t
            await _send_data(port, int(trend_param1.Value),  [i for _ in range(100)])
            await asyncio.sleep(1)
            if i != calls - 2:
                t += 1
            else:
                t = t_start

    server_task.cancel()

    trend_data = _get_trend_data_records()
    assert _get_trend_data_records_count() == calls - 1
    data = trend_data[0][0].Data
    data = struct.unpack("H" * 100, data)
    assert all(val == 2 for val in data)


@pytest.mark.asyncio
@pytest.mark.parametrize('reset_lds_objects', [add_two_objects], indirect=True)
async def test_profiler_should_write_data_to_database(add_lds_objects):
    port = 5027
    Profiler.init()
    plant = PipePlant()
    plant.last_timestamp = 0
    server_task = asyncio.create_task(run_server(plant, port))
    await asyncio.sleep(0.5)
    calls = 5

    t = math.floor(time.time()) + 0.5

    for i in range(calls):
        await _send_data(port, int(trend_param1.Value), [randint(0, 255) for _ in range(100)])
        await asyncio.sleep(t - time.time() + 1)
        t += 1

    server_task.cancel()

    assert _get_profiler_data_active_trends_count() == 1
