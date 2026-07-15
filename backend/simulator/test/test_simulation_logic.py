import asyncio
import contextlib
import math
import struct
import time
import numpy as np
import pytest
from sqlalchemy import text, select, delete
from sqlalchemy.orm import Session
from database.models import lds
from db import get_engine
from simulator.simulation_manager import SimulationManager


PIPELINE_LENGTH = 250
RESOLUTION = 5


def add_objects():
    trend_def = lds.TrendDef(ID='QUICK', Name='TrendDefName')
    unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3', Multiplier=1.0)
    unit_flow = lds.Unit(ID='m3_s', Name='volume flow', Symbol='m3/s', Multiplier=1.0)
    trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                      UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    flow_trend = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=-1, RawMax=1, ScaledMin=0, ScaledMax=100,
                           UnitID=unit_flow.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    simulation_def = lds.SimulationDef(ID='DENSITY_VOLUME_PCHIP', Name='SimulationDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID=simulation_def.ID)
    width_param_def = lds.SimulationParamDef(ID='WIDTH', SimulationDefID=simulation_def.ID)
    flow_trend_param_def = lds.SimulationParamDef(ID='FLOW_TREND_ID', SimulationDefID=simulation_def.ID)
    simulation = lds.Simulation(ID=1, SimulationDefID=simulation_def.ID, TrendID=1, Name='Sim', RefreshTimeSeconds=1,
                                ResolutionMeters=RESOLUTION)
    pipeline_length_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                                SimulationParamDefID=length_param_def.ID, Value=PIPELINE_LENGTH)
    width_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                      SimulationParamDefID=width_param_def.ID, Value=1.1283)
    flow_trend_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                           SimulationParamDefID=flow_trend_param_def.ID, Value=2)
    lds_objects = [[trend_def], [unit_density, unit_flow], [trend_group], [trend, flow_trend], [simulation_def],
                   [length_param_def, flow_trend_param_def, width_param_def],
                   [simulation], [pipeline_length_param, flow_trend_param, width_param]]

    return lds_objects


def add_objects_with_time_delta():
    trend_def = lds.TrendDef(ID='QUICK', Name='TrendDefName')
    unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3', Multiplier=1.0)
    unit_flow = lds.Unit(ID='m3_s', Name='volume flow', Symbol='m3/s', Multiplier=1.0)
    trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                      UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend', TimeDelta=5)
    flow_trend = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=-1, RawMax=1, ScaledMin=0, ScaledMax=100,
                           UnitID=unit_flow.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    simulation_def = lds.SimulationDef(ID='DENSITY_VOLUME_PCHIP', Name='SimulationDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID=simulation_def.ID)
    width_param_def = lds.SimulationParamDef(ID='WIDTH', SimulationDefID=simulation_def.ID)
    flow_trend_param_def = lds.SimulationParamDef(ID='FLOW_TREND_ID', SimulationDefID=simulation_def.ID)
    simulation = lds.Simulation(ID=1, SimulationDefID=simulation_def.ID, TrendID=1, Name='Sim', RefreshTimeSeconds=1,
                                ResolutionMeters=RESOLUTION)
    pipeline_length_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                                SimulationParamDefID=length_param_def.ID, Value=PIPELINE_LENGTH)
    width_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                      SimulationParamDefID=width_param_def.ID, Value=1.1283)
    flow_trend_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                           SimulationParamDefID=flow_trend_param_def.ID, Value=2)
    lds_objects = [[trend_def], [unit_density, unit_flow], [trend_group], [trend, flow_trend], [simulation_def],
                   [length_param_def, flow_trend_param_def, width_param_def],
                   [simulation], [pipeline_length_param, flow_trend_param, width_param]]

    return lds_objects


def add_flow_data(t, timestamp):
    data = np.flip([t+1] * 100)
    data = data.astype(np.uint16)
    packed_data = struct.pack('<100H', *data)

    insert_stmt = text(f"EXEC Update_Insert_TrendData 2, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(insert_stmt, {"data": packed_data})
        session.commit()


def add_const_trend_data(timestamp):
    data = np.flip(1000 * np.ones(100))
    data = data.astype(np.uint16)
    packed_data = struct.pack('<100H', *data)

    insert_stmt = text(f"EXEC Update_Insert_TrendData 1, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(insert_stmt, {"data": packed_data})
        session.commit()


def add_trend_data(t, timestamp):
    data = np.flip([1000+t*100+i for i in range(100)])
    data = data.astype(np.uint16)
    packed_data = struct.pack('<100H', *data)

    statement = text(f"EXEC Update_Insert_TrendData 1, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(statement, {"data": packed_data})
        session.commit()


def add_incorrect_trend_data(timestamp):
    data = np.zeros(100)
    data = data.astype(np.uint16)
    packed_data = struct.pack('<100H', *data)

    insert_stmt = text(f"EXEC Update_Insert_TrendData 1, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(insert_stmt, {"data": packed_data})
        session.commit()


def add_incorrect_flow_data(timestamp):
    data = np.flip([-i for i in range(100)])
    data = data.astype(np.int16)
    packed_data = struct.pack('<100h', *data)

    insert_stmt = text(f"EXEC Update_Insert_TrendData 2, {timestamp}, :data")
    with Session(get_engine()) as session:
        session.execute(insert_stmt, {"data": packed_data})
        session.commit()


def get_simulation_data():
    with Session(get_engine()) as session:
        simulation_data = session.execute(select(lds.SimulationData)).all()

    return [d[0].Data for d in simulation_data]


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
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_both_trends_data_are_regularly_saved(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time):
            add_flow_data(i+time_buffer, t)
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_no_new_trend_data(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_trend_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time1 = 5
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time1):
            add_flow_data(i+time_buffer, t)
            add_trend_data(i+time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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

        sim_time2 = 7
        for i in range(sim_time2):
            add_flow_data(i+sim_time1+time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if stage == 1:
                stage = 2
            elif stage == 2:
                assert previous_data != data
                stage = 1
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_no_trend_data(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time1 = 5
        expected_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        for i in range(sim_time1):
            add_flow_data(i+time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)
        assert data == expected_data

        sim_time2 = 5
        for i in range(sim_time2):
            add_const_trend_data(t)
            add_flow_data(i+sim_time1+time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)
        assert data != expected_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_no_new_trend_data_and_no_trend_data_in_db(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_trend_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time1 = 5
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time1):
            add_flow_data(i+time_buffer, t)
            add_trend_data(i+time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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

        statement = delete(lds.TrendData).where(lds.TrendData.TrendID == 1) # noqa
        with Session(get_engine()) as session:
            session.execute(statement)
            session.commit()

        sim_time2 = 5
        for i in range(sim_time2):
            add_flow_data(i+sim_time1+time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if stage == 1:
                stage = 2
            elif stage == 2:
                assert previous_data != data
                stage = 1
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_both_trends_data_are_stopped(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time1 = 5
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time1):
            add_flow_data(i+time_buffer, t)
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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

        sim_time2 = 10
        for i in range(sim_time2):
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if i > 7:
                assert data == previous_data
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_no_both_trends_data(add_test_context, run_simulations_for_test):
    t = math.floor(time.time())
    async with run_simulations_for_test():
        sim_time = 5
        expected_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        for i in range(sim_time):
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            assert data == expected_data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_no_new_flow_data_should_use_older_data_in_max_time_gap(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time1 = 5
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time1):
            add_flow_data(i+time_buffer, t)
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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

        sim_time2 = 6
        for i in range(sim_time2):
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if stage == 1:
                stage = 2
            elif stage == 2:
                assert previous_data != data
                stage = 1
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_no_flow_data(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time1 = 2
        expected_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        for i in range(sim_time1):
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)
        assert data == expected_data

        sim_time2 = 8
        for i in range(sim_time2):
            add_const_trend_data(t)
            add_flow_data(i+time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)
        assert data != expected_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_no_new_flow_data_should_not_use_older_data_over_max_time_gap(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time1 = 6
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time1):
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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

        sim_time2 = 4
        for i in range(sim_time2):
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            assert previous_data == data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_trend_data_is_not_regularly_saved(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        if i == 1:
            add_trend_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time):
            add_flow_data(i+time_buffer, t)
            if i % 2 == 1:
                add_trend_data(i+time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_flow_trend_data_is_not_regularly_saved(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        if i % 2 == 0:
            add_flow_data(i, t)
        add_trend_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time):
            add_trend_data(i+time_buffer, t)
            if i % 3 == 2:
                add_flow_data(i + time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_both_trends_data_are_not_regularly_saved(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        if i == 0:
            add_flow_data(i, t)
        if i == 1:
            add_trend_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time):
            if i % 2 == 0:
                add_flow_data(i+time_buffer, t)
            if i % 4 == 2:
                add_trend_data(i + time_buffer, t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects_with_time_delta], indirect=True)
async def test_simulation_logic_when_trend_has_time_delta(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time):
            add_flow_data(i+time_buffer, t)
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if i < 4:
                assert data == previous_data
            elif stage == 0 and previous_data != data:
                stage = 1
            elif stage == 1:
                stage = 2
            elif stage == 2:
                assert previous_data != data
                stage = 1
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_trend_writer_saves_data_with_past_timestamps(add_test_context, run_simulations_for_test):
    time_buffer = 3
    time_diff = 10
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t-time_diff)
        add_const_trend_data(t-time_diff)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        expected_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        for i in range(sim_time):
            add_flow_data(i+time_buffer, t-time_diff)
            add_const_trend_data(t-time_diff)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            assert data == expected_data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_trend_writer_saves_data_with_future_timestamps(add_test_context, run_simulations_for_test):
    time_buffer = 3
    time_diff = 8
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t+time_diff)
        add_const_trend_data(t+time_diff)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 12
        expected_data = get_simulation_data()
        for i in range(sim_time):
            add_flow_data(i+time_buffer, t+time_diff)
            add_const_trend_data(t+time_diff)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if i < time_diff:
                assert data == expected_data
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        assert data != expected_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_trend_data_have_incorrect_values(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time):
            add_flow_data(i+time_buffer, t)
            add_incorrect_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
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


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_flow_trend_data_have_incorrect_values(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time):
            add_incorrect_flow_data(t)
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if stage == 0 and previous_data != data:
                stage = 1
            elif stage == 1:
                assert previous_data == data
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_logic_when_flow_trend_data_is_changing(add_test_context, run_simulations_for_test):
    time_buffer = 3
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time1 = 6
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        stage = 0
        for i in range(sim_time1):
            add_incorrect_flow_data(t)
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if stage == 0 and previous_data != data:
                stage = 1
            elif stage == 1:
                assert previous_data == data
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        sim_time2 = 8
        stage = 0
        for i in range(sim_time2):
            add_flow_data(i+time_buffer+sim_time1, t)
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            if i == 0:
                assert previous_data == data
            elif stage == 0 and previous_data != data:
                stage = 1
            elif stage == 1:
                stage = 2
            elif stage == 2:
                assert previous_data != data
                stage = 1
            previous_data = data
            t += 1
            await asyncio.sleep(t - time.time() + 1)


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_calculate_simulation_data_on_start_correctly(add_test_context, run_simulations_for_test):
    time_buffer = 5
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        data = previous_data
        i = 0
        while i < sim_time and data == previous_data:
            i += 1
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        assert data != previous_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_not_calculate_simulation_data_on_start_when_no_trend_data(add_test_context, run_simulations_for_test):
    time_buffer = 5
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        data = previous_data
        i = 0
        while i < sim_time and data == previous_data:
            i += 1
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        assert data == previous_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_not_calculate_simulation_data_on_start_when_no_flow_data(add_test_context, run_simulations_for_test):
    time_buffer = 5
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        data = previous_data
        i = 0
        while i < sim_time and data == previous_data:
            i += 1
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        assert data == previous_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_calculate_simulation_data_on_start_when_no_old_density_data(add_test_context, run_simulations_for_test):
    time_buffer = 5
    t = math.floor(time.time())
    for i in range(time_buffer):
        add_flow_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        data = previous_data
        i = 0
        while i < sim_time and data == previous_data:
            i += 1
            add_const_trend_data(t)
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        assert data != previous_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_calculate_simulation_data_on_start_when_density_data_have_gap(add_test_context, run_simulations_for_test):
    time_buffer = 5
    t = math.floor(time.time())
    for i in range(time_buffer):
        if i < 3:
            add_const_trend_data(t)
        add_flow_data(i, t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        data = previous_data
        i = 0
        while i < sim_time and data == previous_data:
            i += 1
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        assert data != previous_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_calculate_simulation_data_on_start_when_flow_data_have_gap_within_maximum_gap(add_test_context, run_simulations_for_test):
    time_buffer = 5
    t = math.floor(time.time())
    for i in range(time_buffer):
        if i < 3:
            add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        data = previous_data
        i = 0
        while i < sim_time and data == previous_data:
            i += 1
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        assert data != previous_data


@pytest.mark.asyncio
@pytest.mark.parametrize('add_test_context', [add_objects], indirect=True)
async def test_simulation_not_calculate_simulation_data_on_start_when_flow_data_have_gap_over_maximum_gap(add_test_context, run_simulations_for_test):
    time_buffer = 5
    t = math.floor(time.time())
    for i in range(time_buffer):
        if i < 2:
            add_flow_data(i, t)
        add_const_trend_data(t)
        t += 1
        await asyncio.sleep(t - time.time() + 1)

    async with run_simulations_for_test():
        sim_time = 10
        previous_data = [0] * (PIPELINE_LENGTH // RESOLUTION)
        data = previous_data
        i = 0
        while i < sim_time and data == previous_data:
            i += 1
            data = get_simulation_data()
            assert len(data) == PIPELINE_LENGTH // RESOLUTION
            t += 1
            await asyncio.sleep(t - time.time() + 1)

        assert data != previous_data
