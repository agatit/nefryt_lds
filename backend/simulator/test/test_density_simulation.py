import random
import struct
from unittest.mock import patch
import numpy as np
import pytest
from database.models import lds
from simulator.simulations.density_mass import SimulationDensityPCHIPMass, SimulationDensityRKMass
from simulator.simulations.density_volume import SimulationDensityRKVolume, SimulationDensityPCHIPVolume

random.seed(42)
saved_results = []
timestamp_offset = 10

def reset_all_objects():
    trend_def = lds.TrendDef(ID='TrendDefID', Name='TrendDefName')
    unit_density = lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3', Multiplier=1.0)
    trend_group = lds.TrendGroup(ID=1, Name='TrendGroup')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                      UnitID=unit_density.ID, TrendGroupID=trend_group.ID, Color='Color', Name='Trend')

    lds_objects = [[trend_def], [unit_density], [trend_group], [trend]]

    return lds_objects


@pytest.fixture(scope="function", autouse=True)
def reset_saved_results(request):
    global saved_results
    saved_results = []


def mock_save(_, data, timestamp):
    data = data.astype(np.uint16)
    data = np.minimum(data, [np.iinfo(np.uint16).max - 1] * len(data))
    packed_data = struct.pack('<100H', *data)

    unpacked_data = struct.unpack('<100h', packed_data)
    saved_results.append((unpacked_data, timestamp))

d0 = 2
f = 1
length = 10

def mock_read_params(self):
    self.params = {'LENGTH': length, 'WIDTH': 1.1283, 'FLOW_TREND_ID': 2}

def mock_get_current_flow_data(_):
    return lambda t: f + ((np.array(t) - np.floor(t)) / 1) * 0

def mock_get_current_density_data(_):
    return d0 * np.ones(20)

def mock_read_trend(_, trend_id: int):
    if trend_id == 1:
        return lds.Trend(ID=1, TrendDefID='TrendDefID', RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100,
                         UnitID='kg_m3', TrendGroupID=1, Color='Color', Name='Trend')
    else:
        return lds.Trend(ID=2, TrendDefID='TrendDefID', RawMin=1, RawMax=10, ScaledMin=1, ScaledMax=100,
                         UnitID='kg_m3', TrendGroupID=1, Color='Color', Name='Trend')

def mock_read_unit(_, __):
    return lds.Unit(ID='kg_m3', Name='density', Symbol='kg/m3')

def density_and_flow_are_const_tests(simulation_class: type):
    with patch.object(simulation_class, '_read_params', new=mock_read_params):
        with patch.object(simulation_class, '_get_current_flow_data', new=mock_get_current_flow_data):
            with patch.object(simulation_class, '_get_current_density_data', new=mock_get_current_density_data):
                with patch.object(simulation_class, '_read_trend', new=mock_read_trend):
                    with patch.object(simulation_class, '_read_unit', new=mock_read_unit):
                        simulation = lds.Simulation(ID=1, SimulationDefID='SimDefID', TrendID=1, Name='Sim',
                                                    RefreshTimeSeconds=5, ResolutionMeters=10)
                        sim = simulation_class(simulation)
                        sim.simulation_timestamp = 1

                        previous_simulation_data = np.zeros_like(sim.simulation_data)
                        last_non_zero = 0
                        ts = 1
                        while not np.isclose(sim.simulation_data, np.ones_like(sim.simulation_data) * d0, atol=1e-2).all() and ts < 200:
                            sim.calculate_simulation_data()
                            assert not np.any(np.isnan(sim.simulation_data))
                            assert not np.allclose(sim.simulation_data, 0)
                            assert not np.array_equal(sim.simulation_data, previous_simulation_data)
                            assert last_non_zero <= np.max(np.nonzero(np.round(sim.simulation_data, decimals=3)))
                            last_non_zero = np.max(np.nonzero(np.round(sim.simulation_data, decimals=3)))
                            previous_simulation_data = np.copy(np.round(sim.simulation_data, decimals=3))
                            ts += 1
                            sim.simulation_timestamp = ts

                        assert length + 1 <= ts <= length + 5

                        prev_exact_values_count = 0
                        while ts < 25:
                            sim.calculate_simulation_data()
                            exact_values_count = np.sum(np.round(sim.simulation_data, decimals=3) == d0)
                            assert prev_exact_values_count <= exact_values_count
                            assert np.isclose(sim.simulation_data[:-1], np.ones_like(sim.simulation_data[:-1]) * d0, atol=1e-2).all()
                            prev_exact_values_count = exact_values_count
                            ts += 1
                            sim.simulation_timestamp = ts

def test_density_volume_rk_simulation_simulates_correctly_when_density_and_flow_are_const():
    global f
    f = 1
    density_and_flow_are_const_tests(SimulationDensityRKVolume)


def test_density_volume_pchip_simulation_simulates_correctly_when_density_and_flow_are_const():
    global f
    f = 1
    density_and_flow_are_const_tests(SimulationDensityPCHIPVolume)


def test_density_volume_pchip_simulation_simulates_correctly_when_density_is_changing():
    pass


def test_density_volume_rk_simulation_simulates_correctly_when_density_is_changing():
    pass


def test_density_volume_pchip_simulation_simulates_correctly_when_flow_is_changing():
    pass


def test_density_volume_rk_simulation_simulates_correctly_when_flow_is_changing():
    pass


def test_density_mass_rk_simulation_simulates_correctly_when_density_and_flow_are_const():
    global f
    f = 2
    density_and_flow_are_const_tests(SimulationDensityRKMass)


def test_density_mass_pchip_simulation_simulates_correctly_when_density_and_flow_are_const():
    global f
    f = 2
    density_and_flow_are_const_tests(SimulationDensityPCHIPMass)


def test_density_mass_pchip_simulation_simulates_correctly_when_density_is_changing():
    pass


def test_density_mass_rk_simulation_simulates_correctly_when_density_is_changing():
    pass


def test_density_mass_pchip_simulation_simulates_correctly_when_flow_is_changing():
    pass


def test_density_mass_rk_simulation_simulates_correctly_when_flow_is_changing():
    pass

