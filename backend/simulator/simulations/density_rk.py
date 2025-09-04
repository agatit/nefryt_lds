import numpy as np
from scipy.integrate import solve_ivp
from simulator.simulations.density import SimulationDensityBase


class SimulationDensityRKBase(SimulationDensityBase):
    def _refresh_simulation_data(self, timestamp: int):
        sol = solve_ivp(fun=self._deriv, t_span=[timestamp, timestamp + 1], y0=self.simulation_data)
        self.simulation_data = sol.y[:, -1] # noqa

    def _deriv(self, t: float, y: np.array):
        self.pipe_density_gradient = - np.diff(y, prepend=self.density_interp(t)) / self.simulation_segment_length
        pipe_velocity = self.calculate_velocity(self.flow_interp(t), self.density_interp(t))
        return pipe_velocity * self.pipe_density_gradient
