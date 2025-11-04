import pytest
from database.models import lds
from simulator.simulations.base import SimulationBase

trend_def = lds.TrendDef(ID='TrendDefID', Name='TrendDefName')
unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3')
unit_flow = lds.Unit(ID='m3_s', Name='volume flow', Symbol='m3/s')
trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                  UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
flow_trend = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                       UnitID=unit_flow.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
simulation_def = lds.SimulationDef(ID='SimDefID', Name='SimDefName')
length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='SimDefID')
flow_trend_param_def = lds.SimulationParamDef(ID='FLOW_TREND_ID', SimulationDefID='SimDefID')
simulation = lds.Simulation(ID=1, SimulationDefID='SimDefID', TrendID=1, Name='Sim', RefreshTimeSeconds=5, ResolutionMeters=100)
pipeline_length_param = lds.SimulationParam(SimulationDefID='SimDefID', SimulationID=simulation.ID, SimulationParamDefID='LENGTH', Value=1000)
flow_trend_param = lds.SimulationParam(SimulationDefID='SimDefID', SimulationID=simulation.ID, SimulationParamDefID='FLOW_TREND_ID', Value=2)
lds_objects = [[trend_def], [unit_density, unit_flow], [trend, flow_trend], [simulation_def],
               [length_param_def, flow_trend_param_def], [simulation], [pipeline_length_param, flow_trend_param]]


def reset_all_objects():
    global lds_objects, simulation, pipeline_length_param, simulation_def, length_param_def, trend_def, trend, \
        flow_trend_param_def, flow_trend_param, flow_trend, unit_density, unit_flow,trend_group
    trend_def = lds.TrendDef(ID='TrendDefID', Name='TrendDefName')
    unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3', Multiplier=1.0)
    unit_flow = lds.Unit(ID='m3_s', Name='volume flow', Symbol='m3/s', Multiplier=1.0)
    trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                      UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    flow_trend = lds.Trend(ID=2, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                           UnitID=unit_flow.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    simulation_def = lds.SimulationDef(ID='SimDefID', Name='SimDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID=simulation_def.ID)
    flow_trend_param_def = lds.SimulationParamDef(ID='FLOW_TREND_ID', SimulationDefID='SimDefID')
    simulation = lds.Simulation(ID=1, SimulationDefID='SimDefID', TrendID=1, Name='Sim', RefreshTimeSeconds=5,
                                ResolutionMeters=100)
    pipeline_length_param = lds.SimulationParam(SimulationDefID='SimDefID', SimulationID=simulation.ID,
                                                SimulationParamDefID='LENGTH', Value=1000)
    flow_trend_param = lds.SimulationParam(SimulationDefID='SimDefID', SimulationID=simulation.ID,
                                           SimulationParamDefID='FLOW_TREND_ID', Value=2)
    lds_objects = [[trend_def], [trend_group], [unit_density, unit_flow], [trend, flow_trend], [simulation_def],
                   [length_param_def, flow_trend_param_def], [simulation], [pipeline_length_param, flow_trend_param]]

    return lds_objects


def reset_objects1():
    global lds_objects, simulation, simulation_def, length_param_def, trend_def, trend, unit_density, trend_group
    trend_def = lds.TrendDef(ID='TrendDefID', Name='TrendDefName')
    unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3', Multiplier=1.0)
    trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                      UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    simulation_def = lds.SimulationDef(ID='SimDefID', Name='SimDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID=simulation_def.ID)
    simulation = lds.Simulation(ID=1, SimulationDefID=simulation_def.ID, TrendID=1, Name='Sim', RefreshTimeSeconds=5,
                                ResolutionMeters=100)

    lds_objects = [[trend_def], [unit_density], [trend_group], [trend], [simulation_def], [length_param_def], [simulation]]

    return lds_objects


def reset_objects2():
    global lds_objects, simulation, simulation_def, length_param_def, pipeline_length_param, trend_def, trend, \
        unit_density, trend_group
    trend_def = lds.TrendDef(ID='TrendDefID', Name='TrendDefName')
    unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3', Multiplier=1.0)
    trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                      UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    simulation_def = lds.SimulationDef(ID='SimDefID', Name='SimDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID=simulation_def.ID)
    simulation = lds.Simulation(ID=1, SimulationDefID=simulation_def.ID, TrendID=1, Name='Sim', RefreshTimeSeconds=5,
                                ResolutionMeters=100)
    pipeline_length_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                                SimulationParamDefID=length_param_def.ID, Value=0.5)

    lds_objects = [[trend_def], [unit_density], [trend_group], [trend], [simulation_def],
                   [length_param_def], [simulation], [pipeline_length_param]]

    return lds_objects


def reset_objects3():
    global lds_objects, simulation, simulation_def, length_param_def, pipeline_length_param, trend_def, trend, \
        unit_density, trend_group
    trend_def = lds.TrendDef(ID='TrendDefID', Name='TrendDefName')
    unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3', Multiplier=1.0)
    trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                      UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    simulation_def = lds.SimulationDef(ID='SimDefID', Name='SimDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID=simulation_def.ID)
    simulation = lds.Simulation(ID=1, SimulationDefID=simulation_def.ID, TrendID=1, Name='Sim', RefreshTimeSeconds=5,
                                ResolutionMeters=100)
    pipeline_length_param = lds.SimulationParam(SimulationDefID=simulation_def.ID, SimulationID=simulation.ID,
                                                SimulationParamDefID=length_param_def.ID, Value=1000)

    lds_objects = [[trend_def], [unit_density], [trend_group], [trend], [simulation_def],
                   [length_param_def], [simulation], [pipeline_length_param]]

    return lds_objects

def reset_objects4():
    global lds_objects, simulation, simulation_def, length_param_def, pipeline_length_param, trend_def, trend, \
        unit_density, trend_group, flow_trend_param, flow_trend_param_def
    trend_def = lds.TrendDef(ID='TrendDefID', Name='TrendDefName')
    unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3', Multiplier=1.0)
    trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                      UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')
    simulation_def = lds.SimulationDef(ID='SimDefID', Name='SimDefName')
    length_param_def = lds.SimulationParamDef(ID='LENGTH', SimulationDefID='SimDefID')
    flow_trend_param_def = lds.SimulationParamDef(ID='FLOW_TREND_ID', SimulationDefID='SimDefID')
    simulation = lds.Simulation(ID=1, SimulationDefID='SimDefID', TrendID=1, Name='Sim', RefreshTimeSeconds=5,
                                ResolutionMeters=100)
    pipeline_length_param = lds.SimulationParam(SimulationDefID='SimDefID', SimulationID=simulation.ID,
                                                SimulationParamDefID='LENGTH', Value=1000)
    flow_trend_param = lds.SimulationParam(SimulationDefID='SimDefID', SimulationID=simulation.ID,
                                           SimulationParamDefID='FLOW_TREND_ID', Value=2)

    lds_objects = [[trend_def], [unit_density], [trend_group], [trend], [simulation_def], [length_param_def, flow_trend_param_def],
                   [simulation], [pipeline_length_param, flow_trend_param]]

    return lds_objects


@pytest.mark.parametrize('reset_lds_objects', [reset_objects1], indirect=True)
def test_simulation_base_should_raise_exception_when_no_pipeline_length_param(add_lds_objects):
    with pytest.raises(ValueError, match=f'No \'LENGTH\' param in simulation with id = {simulation.ID}'):
        SimulationBase(simulation, '')


@pytest.mark.parametrize('reset_lds_objects', [reset_objects2], indirect=True)
def test_simulation_base_should_raise_exception_when_pipeline_length_param_is_not_integer(add_lds_objects):
    with pytest.raises(ValueError, match=f'\'LENGTH\' param in simulation with id = {simulation.ID} has to be an integer'):
        SimulationBase(simulation, '')


@pytest.mark.parametrize('reset_lds_objects', [reset_objects3], indirect=True)
def test_simulation_base_should_raise_exception_when_no_flow_trend_param(add_lds_objects):
    with pytest.raises(ValueError, match=f'No param \'FLOW_TREND_ID\' in simulation with id = {simulation.ID}'):
        SimulationBase(simulation, '')


@pytest.mark.parametrize('reset_lds_objects', [reset_objects4], indirect=True)
def test_simulation_base_should_raise_exception_when_no_trend_with_given_flow_trend_id(add_lds_objects):
    with pytest.raises(ValueError, match=f'No flow trend with id = {flow_trend_param.Value} in simulation with id = {simulation.ID}'):
        SimulationBase(simulation, '')


@pytest.mark.parametrize('reset_lds_objects', [reset_all_objects], indirect=True)
def test_simulation_base_should_start_correctly(add_lds_objects):
    sim = SimulationBase(simulation, '')
    assert sim.lds_simulation == simulation
    assert sim.pipeline_length == int(pipeline_length_param.Value)
    assert sim.simulation_trend == trend
    assert sim.simulation_unit == unit_density
    assert sim.flow_trend == flow_trend
    assert sim.distances == [i*sim.lds_simulation.ResolutionMeters for i in range(sim.pipeline_length // sim.lds_simulation.ResolutionMeters)]


def test_simulation_base_should_save_simulation_data_correctly():
    pass
