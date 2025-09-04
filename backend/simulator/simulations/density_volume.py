import numpy as np
from simulator.simulations.density_pchip import SimulationDensityPCHIPBase
from simulator.simulations.density_rk import SimulationDensityRKBase


class SimulationDensityRKVolume(SimulationDensityRKBase):
    def calculate_velocity(self, flow_data: np.ndarray, _) -> np.ndarray:
        return flow_data / self.pipeline_area


class SimulationDensityPCHIPVolume(SimulationDensityPCHIPBase):
    def calculate_velocity(self, flow_data: np.ndarray, _) -> np.ndarray:
        return flow_data / self.pipeline_area
