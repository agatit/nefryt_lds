import numpy as np
from scipy.interpolate import PchipInterpolator
from simulator.simulations.density import SimulationDensityBase


class SimulationDensityPCHIPBase(SimulationDensityBase):
    def _refresh_simulation_data(self, timestamp: int):
        substeps = 5
        dx = self.pipeline_length / len(self.simulation_data)
        arr_x = np.arange(len(self.simulation_data))

        dt = 1 / substeps
        for substep in range(substeps):
            t0 = timestamp + substep * dt
            t1 = t0 + dt
            timestamps = np.linspace(t0, t1, 11)
            flows = self.flow_interp(timestamps)
            flow_in_step = np.trapezoid(flows, timestamps)
            # TODO: prepare density_data
            velocity = self.calculate_velocity(flow_in_step, None)
            dists_in_cells = velocity / dx
            d0 = float(self.density_interp(0.5 * (t0 + t1)))

            interp = PchipInterpolator(
                arr_x,
                self.simulation_data,
                extrapolate=True
            )
            y_new: np.ndarray = interp(arr_x - dists_in_cells)
            y_new[arr_x - dists_in_cells < 0] = d0

            self.simulation_data = y_new
