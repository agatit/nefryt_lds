import math

from simulator.simulations.density import SimulationDensityBase


class SimulationDensityMass(SimulationDensityBase):
    def calculate_velocity(self, flow: float, density: float) -> float | None:
        area = (self.pipeline_width/2)**2 * math.pi
        return flow / (density * area)