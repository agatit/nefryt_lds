import numpy as np
from scipy.interpolate import interp1d
from simulator.simulations.density_pchip import SimulationDensityPCHIPBase
from simulator.simulations.density_rk import SimulationDensityRKBase


class SimulationDensityRKMass(SimulationDensityRKBase):
    def _calculate_volume_covered(self, flows: list, densities: list, last_timestamp: int, buffer_size: int) -> float:
        volume_covered = 0
        for i, (one_sec_flow_interp, one_sec_density) in enumerate(zip(flows, densities)):
            flow_timestamps = np.arange(last_timestamp - buffer_size + i + 1, last_timestamp - buffer_size + i + 2, 100)
            density_timestamps = np.linspace(self.simulation_timestamp, self.simulation_timestamp + 1, len(one_sec_density))
            one_sec_density_interp = interp1d(density_timestamps, one_sec_density, kind='linear', fill_value='extrapolate')
            one_sec_flow = one_sec_flow_interp(flow_timestamps)
            one_sec_density = one_sec_density_interp(flow_timestamps)
            one_sec_flow = one_sec_flow / one_sec_density
            volume_covered += np.mean(one_sec_flow)

        return volume_covered

    def calculate_velocity(self, flow_data: np.ndarray, density_data: np.ndarray) -> np.ndarray:
        return flow_data / (density_data * self.pipeline_area)


class SimulationDensityPCHIPMass(SimulationDensityPCHIPBase):
    def _calculate_volume_covered(self, flows: list, densities: list, last_timestamp: int, buffer_size: int) -> float:
        volume_covered = 0
        for i, (one_sec_flow_interp, one_sec_density) in enumerate(zip(flows, densities)):
            flow_timestamps = np.arange(last_timestamp - buffer_size + i + 1, last_timestamp - buffer_size + i + 2, 100)
            density_timestamps = np.linspace(self.simulation_timestamp, self.simulation_timestamp + 1, len(one_sec_density))
            one_sec_density_interp = interp1d(density_timestamps, one_sec_density, kind='linear', fill_value='extrapolate')
            one_sec_flow = one_sec_flow_interp(flow_timestamps)
            one_sec_density = one_sec_density_interp(flow_timestamps)
            one_sec_flow = one_sec_flow / one_sec_density
            volume_covered += np.mean(one_sec_flow)

        return volume_covered

    def calculate_velocity(self, flow_data: np.ndarray, density_data: np.ndarray) -> np.ndarray:
        return flow_data / (density_data * self.pipeline_area)
