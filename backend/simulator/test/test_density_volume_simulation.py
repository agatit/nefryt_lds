import random
import struct
from unittest.mock import patch
import numpy as np
import pytest
from database.models import lds
from simulator.simulations.density_volume import SimulationDensityVolume

random.seed(42)
saved_results = []
timestamp_offset = 10

def reset_all_objects():
    trend_def = lds.TrendDef(ID='TrendDefID', Name='TrendDefName')
    unit = lds.Unit(ID='Density')
    trend = lds.Trend(ID=1, TrendDefID=trend_def.ID, RawMin=0, RawMax=1, ScaledMin=0, ScaledMax=100, UnitID=unit.ID)

    lds_objects = [[trend_def], [unit], [trend]]

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


def test_density_volume_simulation_simulates_correctly_when_density_and_flow_are_const():
    d0 = 2*np.ones(20)
    flow = 1*np.ones(20)

    def mock_read_params(self):
        self.params = {'LENGTH': 100, 'WIDTH': 1.1283, 'FLOW_TREND': 2}

    def mock_get_current_data(_, __):
        return flow, d0

    def mock_read_trend(_):
        return lds.Trend(ID=1, TrendDefID='TrendDefID', RawMin=1, RawMax=10, ScaledMin=1, ScaledMax=100)

    def mock_read_unit(_):
        return lds.Unit(ID='kg/m3')

    def mock_read_flow_trend(self, __):
        self.flow_trend = lds.Trend(ID=2, TrendDefID='TrendDefID', RawMin=1, RawMax=10, ScaledMin=1, ScaledMax=100)

    with patch.object(SimulationDensityVolume, '_read_params', new=mock_read_params):
        with patch.object(SimulationDensityVolume, '_get_current_data', new=mock_get_current_data):
            with patch.object(SimulationDensityVolume, '_read_trend', new=mock_read_trend):
                with patch.object(SimulationDensityVolume, '_read_unit', new=mock_read_unit):
                    with patch.object(SimulationDensityVolume, '_read_flow_trend', new=mock_read_flow_trend):
                        simulation = lds.Simulation(ID=1, SimulationDefID='SimDefID', TrendID=1, Name='Sim', RefreshTimeSeconds=5, ResolutionMeters=10)
                        sim = SimulationDensityVolume(simulation, '')

                        previous_simulation_data = np.zeros_like(sim.simulation_data)
                        t = 1
                        while not np.isclose(sim.simulation_data[0], d0[0], atol=1e-3):
                            sim.calculate_simulation_data(t)
                            assert not np.any(np.isnan(sim.simulation_data))
                            assert not np.allclose(sim.simulation_data, 0)
                            assert not np.array_equal(sim.simulation_data, previous_simulation_data)
                            assert np.all((sim.simulation_data-previous_simulation_data) >= 0)
                            previous_simulation_data = np.copy(sim.simulation_data)
                            print(t)
                            t += 1

                        previous_correct_data_count = 1
                        while previous_correct_data_count != len(sim.simulation_data):
                            sim.calculate_simulation_data(t)
                            assert np.count_nonzero(np.isclose(sim.simulation_data, d0[0] * np.ones_like(sim.simulation_data), atol=1e-2)) >= previous_correct_data_count
                            previous_correct_data_count = np.count_nonzero(np.isclose(sim.simulation_data, d0[0] * np.ones_like(sim.simulation_data), atol=1e-2))
                            t += 1


# TODO: test ze zmiennym przepływem
# TODO: test ze zmienną gęstością
