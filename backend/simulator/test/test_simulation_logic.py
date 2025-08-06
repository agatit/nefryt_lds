import asyncio
import math
import struct
import time

import numpy as np
import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from database.models import lds
from db import get_engine
from simulator.simulation_manager import SimulationManager


def add_objects():
    trend_def = lds.TrendDef(ID='QUICK', Name='TrendDefName')
    unit = lds.Unit(ID='DensityUnit')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100, UnitID=unit.ID)
    simulation_def = lds.SimulationDef(ID='DENSITY_VOLUME', Name='SimulationDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID=simulation_def.ID)
    flow_trend_param_def = lds.SimulationParamDef(ID='FLOW_TREND', SimulationDefID=simulation_def.ID)
    simulation = lds.Simulation(ID=1, SimulationDefID='SimDefID', TrendID=1, Name='Sim', RefreshTimeSeconds=2,
                                ResolutionMeters=10)
    pipeline_length_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                                SimulationParamDefID=length_param_def.ID, Value=100)
    flow_trend_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                           SimulationParamDefID=flow_trend_param_def.ID, Value=2)
    flow_trend = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100)
    lds_objects = [[trend_def], [unit], [trend, flow_trend], [simulation_def], [length_param_def, flow_trend_param_def],
                   [simulation], [pipeline_length_param, flow_trend_param]]

    return lds_objects


def add_flow_data(t, timestamp):
    data = np.array([t*20 + i//5 for i in range(100)])
    data = data.astype(np.uint16)
    packed_data = struct.pack('<100H', *data)

    insert_stmt = text(f"EXEC Update_Insert_TrendData 2, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(insert_stmt, {"data": packed_data})
        session.commit()

def add_trend_data(timestamp):
    data = 10 * np.ones(100)
    data = data.astype(np.uint16)
    packed_data = struct.pack('<100H', *data)

    insert_stmt = text(f"EXEC Update_Insert_TrendData 1, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(insert_stmt, {"data": packed_data})
        session.commit()



@pytest.mark.asyncio
@pytest.mark.parametrize('reset_lds_objects', [add_objects], indirect=True)
async def test_simulation_logic_when_both_trends_data_is_correct(add_lds_objects):
    server_task = asyncio.create_task(SimulationManager().start_simulations())
    await asyncio.sleep(2)
    sim_time = 10

    t = math.floor(time.time()) + 0.5
    for i in range(sim_time):
        await _send_data(port, int(trend_param1.Value), [randint(0, 255) for _ in range(100)])
        await asyncio.sleep(t - time.time() + 1)
        t += 1

    server_task.cancel()

    @pytest.mark.asyncio
    @pytest.mark.parametrize('reset_lds_objects', [add_objects], indirect=True)
    async def test_trend_data_should_be_written_to_db_when_correct_address(add_lds_objects):
        port = 5022
        Profiler.init()
        server_task = asyncio.create_task(run_server(PipePlant(), port))
        await asyncio.sleep(5)
        calls = 2

        t = math.floor(time.time()) + 0.5
        for i in range(calls):
            await _send_data(port, int(trend_param1.Value), [randint(0, 255) for _ in range(100)])
            await asyncio.sleep(t - time.time() + 1)
            t += 1

        server_task.cancel()

        assert _get_trend_data_records_count() == calls