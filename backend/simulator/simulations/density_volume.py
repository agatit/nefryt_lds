import numpy as np
from simulator.simulations.density import SimulationDensityBase


class SimulationDensityVolume(SimulationDensityBase):
    def calculate_velocity(self, flow_data: np.ndarray, _) -> np.ndarray:
        return flow_data / self.pipeline_area