import numpy as np
from simulator.simulations.density_pchip import SimulationDensityPCHIPBase
from simulator.simulations.density_rk import SimulationDensityRKBase


class SimulationDensityRKVolume(SimulationDensityRKBase):
    def _calculate_volume_covered(self, flows: list, densities: list, last_timestamp: int, buffer_size: int) -> float:
        volume_covered = 0
        for i, (one_sec_flow_interp, one_sec_density) in enumerate(zip(flows, densities)):
            timestamps = np.arange(last_timestamp - buffer_size + i + 1, last_timestamp - buffer_size + i + 2, 100)
            one_sec_flow = one_sec_flow_interp(timestamps)
            volume_covered += np.mean(one_sec_flow)

        return volume_covered

    def calculate_velocity(self, flow_data: np.ndarray, _) -> np.ndarray:
        return flow_data / self.pipeline_area


class SimulationDensityPCHIPVolume(SimulationDensityPCHIPBase):
    def _calculate_volume_covered(self, flows: list, densities: list, last_timestamp: int, buffer_size: int) -> float:
        volume_covered = 0
        for i, (one_sec_flow_interp, one_sec_density) in enumerate(zip(flows, densities)):
            timestamps = np.arange(last_timestamp - buffer_size + i + 1, last_timestamp - buffer_size + i + 2, 100)
            one_sec_flow = one_sec_flow_interp(timestamps)
            volume_covered += np.mean(one_sec_flow)

        return volume_covered

    def calculate_velocity(self, flow_data: np.ndarray, _) -> np.ndarray:
        return flow_data / self.pipeline_area
