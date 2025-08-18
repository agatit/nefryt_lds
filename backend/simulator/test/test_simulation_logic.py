import asyncio
import contextlib
import math
import struct
import time
import numpy as np
import pytest
from sqlalchemy import text, select
from sqlalchemy.orm import Session
from database.models import lds
from db import get_engine
from simulator.simulation_manager import SimulationManager


def add_objects():
    trend_def = lds.TrendDef(ID='QUICK', Name='TrendDefName')
    unit = lds.Unit(ID='Density')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100, UnitID=unit.ID)
    simulation_def = lds.SimulationDef(ID='DENSITY_VOLUME', Name='SimulationDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID=simulation_def.ID)
    width_param_def = lds.SimulationParamDef(ID='WIDTH', SimulationDefID=simulation_def.ID)
    flow_trend_param_def = lds.SimulationParamDef(ID='FLOW_TREND', SimulationDefID=simulation_def.ID)
    simulation = lds.Simulation(ID=1, SimulationDefID=simulation_def.ID, TrendID=1, Name='Sim', RefreshTimeSeconds=2,
                                ResolutionMeters=10)
    pipeline_length_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                                SimulationParamDefID=length_param_def.ID, Value=100)
    width_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                      SimulationParamDefID=width_param_def.ID, Value=1.1283)
    flow_trend_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                           SimulationParamDefID=flow_trend_param_def.ID, Value=2)
    flow_trend = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100)
    lds_objects = [[trend_def], [unit], [trend, flow_trend], [simulation_def], [length_param_def, flow_trend_param_def, width_param_def],
                   [simulation], [pipeline_length_param, flow_trend_param, width_param]]

    return lds_objects


def add_flow_data(t, timestamp):
    data = np.array([t+1] * 100)
    data = data.astype(np.uint16)
    packed_data = struct.pack('<100H', *data)

    insert_stmt = text(f"EXEC Update_Insert_TrendData 2, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(insert_stmt, {"data": packed_data})
        session.commit()


def add_trend_data(timestamp):
    data = 1000 * np.ones(100)
    data = data.astype(np.uint16)
    packed_data = struct.pack('<100H', *data)

    insert_stmt = text(f"EXEC Update_Insert_TrendData 1, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(insert_stmt, {"data": packed_data})
        session.commit()


def get_simulation_data():
    with Session(get_engine()) as session:
        simulation_data = session.execute(select(lds.SimulationData)).all()

    data = []
    for d in simulation_data:
        data.append(d[0].Data)
        print(d[0].Data, end=' ')
    print()
    return data


def shutdown_processes(simulations):
    for simulation in simulations:
        simulation.process.terminate()
        simulation.process.join(1)


@pytest.fixture
def run_simulations_for_test():
    @contextlib.asynccontextmanager
    async def _start():
        simulations = await SimulationManager().start_simulations()
        try:
            yield simulations
        finally:
            shutdown_processes(simulations)
    return _start


@pytest.mark.asyncio
@pytest.mark.parametrize('reset_lds_objects', [add_objects], indirect=True)
async def test_simulation_logic_when_both_trends_data_is_regularly_saved(add_lds_objects, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    print(f'Save starts at {t}')
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_trend_data(t)
        print(f'Timestamp {t}')
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    # _ = run_simulations_for_test
    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * 10
        stage = 0
        for i in range(sim_time):
            add_flow_data(i+time_buffer, t)
            add_trend_data(t)
            print(f'Timestamp {t}')
            data = get_simulation_data()
            print(data)
            assert len(data) == 10
            if stage == 0 and previous_data != data:
                stage = 1
            elif stage == 1:
                stage = 2
            elif stage == 2:
                assert previous_data != data
                stage = 1
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        print(f'Save ends at {t}')


# @pytest.mark.asyncio
# @pytest.mark.parametrize('reset_lds_objects', [add_objects], indirect=True)
# async def test_simulation_logic_when_both_trends_data_is_regularly_saved(add_lds_objects, run_simulations_for_test):
#     time_buffer = 3
#     t = math.floor(time.time())
#     print(f'Save starts at {t}')
#     for i in range(time_buffer):
#         add_flow_data(i, t)
#         add_trend_data(t)
#         print(f'Timestamp {t}')
#         t += 1
#         await asyncio.sleep(t - time.time() + 1)
#
#     # _ = run_simulations_for_test
#     async with run_simulations_for_test():
#         sim_time = 10
#         previous_data = [0] * 10
#         stage = 0
#         for i in range(sim_time):
#             add_flow_data(i+time_buffer, t)
#             add_trend_data(t)
#             print(f'Timestamp {t}')
#             data = get_simulation_data()
#             print(data)
#             assert len(data) == 10
#             if stage == 0 and previous_data != data:
#                 stage = 1
#             elif stage == 1:
#                 stage = 2
#             elif stage == 2:
#                 assert previous_data != data
#                 stage = 1
#             previous_data = data
#             t += 1
#             await asyncio.sleep(t - time.time() + 1)
#
#         print(f'Save ends at {t}')
#         # shutdown_processes(simulations)
#         assert False
