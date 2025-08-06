import logging
import math
import struct
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from database.models import lds
from db import get_engine
from simulator.simulations.base import SimulationBase


class SimulationDensityBase(SimulationBase):
    def __init__(self, simulation: lds.Simulation, db_uri: str, plot_sim: bool = False):
        super().__init__(simulation, db_uri, plot_sim)

        try:
            pipeline_width = float(self.params['WIDTH'])
        except ValueError:
            raise ValueError(f'\'WIDTH\' param for simulation {self.lds_simulation.ID} must be a float')
        self.pipeline_area = (pipeline_width/2)**2 * math.pi
        self.density_interp = None
        self.velocity_interp = None

    def calculate_simulation_data_on_start(self, current_timestamp: int):
        pass
        # previous_distance = 0
        # timestamp = current_timestamp - 1
        # buffer_size = 100
        # previous_flow = None
        # previous_density = None
        #
        # iter_flow_trend = iter([])
        # iter_density_trend = iter([])
        # flow_trend_data = None
        # density_trend_data = None
        #
        # while True:
        #     if flow_trend_data is None:
        #         statement = (select(lds.TrendData)
        #                     .where(lds.TrendData.TrendID == self.flow_trend.ID) # noqa
        #                     .where(lds.TrendData.Time <= timestamp)
        #                     .order_by(desc(lds.TrendData.Time)) # noqa
        #                     .limit(buffer_size))
        #         with Session(get_engine()) as session:
        #             results_flow_trend = session.execute(statement).scalars().all()
        #
        #         iter_flow_trend = iter(results_flow_trend)
        #         flow_trend_data = next(iter_flow_trend, None)
        #         if flow_trend_data is None:
        #             logging.warning(f'Cannot simulate full data on start of simulation with id={self.lds_simulation.ID} '
        #                             f'cause: not enough flow trend with id={self.flow_trend.ID} data')
        #             break
        #
        #     if self.flow_trend.RawMin >= 0:
        #         one_second_data = struct.unpack("H" * 100, flow_trend_data.Data)
        #     else:
        #         one_second_data = struct.unpack("h" * 100, flow_trend_data.Data)
        #     avg_past_flow = (sum(one_second_data) / len(one_second_data)) / float(self.flow_unit.Multiplier)
        #     if flow_trend_data.Time != timestamp and previous_flow is not None:
        #         delta_flow = (avg_past_flow - previous_flow[0]) / (previous_flow[1] - flow_trend_data.Time)
        #         avg_past_flow = previous_flow[0] + (previous_flow[1] - timestamp) * delta_flow
        #     elif flow_trend_data.Time == timestamp:
        #         previous_flow = (avg_past_flow, flow_trend_data.Time)
        #         flow_trend_data = next(iter_flow_trend, None)
        #     velocity = self.calculate_velocity(avg_past_flow, 0)
        #
        #     if density_trend_data is None:
        #         statement = (select(lds.TrendData)
        #                     .where(lds.TrendData.TrendID == self.simulation_trend.ID)
        #                     .where(lds.TrendData.Time <= timestamp)
        #                     .order_by(desc(lds.TrendData.Time)) # noqa
        #                     .limit(buffer_size))
        #         with Session(get_engine()) as session:
        #             results_density_trend = session.execute(statement).scalars().all()
        #
        #         iter_density_trend = iter(results_density_trend)
        #         density_trend_data = next(iter_density_trend, None)
        #         if density_trend_data is None:
        #             logging.warning(
        #                 f'Cannot simulate full data on start of simulation with id={self.lds_simulation.ID} '
        #                 f'cause: not enough density trend with id={self.simulation_trend.ID} data')
        #             break
        #
        #     if self.simulation_trend.RawMin >= 0:
        #         one_second_data = struct.unpack("H" * 100, density_trend_data.Data)
        #     else:
        #         one_second_data = struct.unpack("h" * 100, density_trend_data.Data)
        #     avg_past_density = (sum(one_second_data) / len(one_second_data)) / float(self.simulation_unit.Multiplier)
        #     density = None
        #     if density_trend_data.Time != timestamp and previous_density is not None:
        #         delta_density = (avg_past_density - previous_density[0]) / (previous_density[1] - density_trend_data.Time)
        #         density = previous_density[0] + (previous_density[1] - timestamp) * delta_density
        #     elif density_trend_data.Time == timestamp:
        #         density = avg_past_density
        #         previous_density = (avg_past_density, density_trend_data.Time)
        #         density_trend_data = next(iter_density_trend, None)
        #
        #     previous_distance += velocity
        #     self.simulation_data.append(SimulatorData(Distance=previous_distance, Data=density))
        #     if previous_distance >= self.pipeline_length:
        #         break
        #     timestamp -= 1

    def calculate_simulation_data(self, current_timestamp: int):
        current_data = self._get_current_data(current_timestamp)
        if current_data:
            flow_data, density_data = current_data
            velocity_data = self.calculate_velocity(flow_data, density_data)
            x = np.linspace(current_timestamp, current_timestamp + 1, len(density_data))
            self.density_interp = interp1d(x, density_data, kind='linear', fill_value='extrapolate')
            self.velocity_interp = interp1d(x, velocity_data, kind='linear', fill_value='extrapolate')
            self._refresh_simulation_data(current_timestamp)

    def _get_current_data(self, current_timestamp: int):
        window_size = 5
        statement_flow = (select(lds.TrendData)
                         .where(lds.TrendData.TrendID == self.flow_trend.ID)  # noqa
                         .where(lds.TrendData.Time <= current_timestamp) # noqa
                         .order_by(desc(lds.TrendData.Time))  # noqa
                         .limit(1))
        statement_density = (select(lds.TrendData)
                            .where(lds.TrendData.TrendID == self.simulation_trend.ID) # noqa
                            .where(lds.TrendData.Time == current_timestamp)) # noqa

        with Session(get_engine()) as session:
            density_trend_data = session.execute(statement_density).scalars().first()
            flow_trend_data = session.execute(statement_flow).scalars().first()

        density_data_mean = None
        if density_trend_data is not None:
            if self.simulation_trend.RawMin >= 0:
                density_data = struct.unpack("H" * 100, density_trend_data.Data)
            else:
                density_data = struct.unpack("h" * 100, density_trend_data.Data)
            density_data_mean = np.array([(sum(density_data[i:i*window_size])/window_size for i in range(100//window_size))])

        if flow_trend_data is None:
            logging.warning(f'No flow trend data for simulation with id={self.lds_simulation.ID}')
            return None
        else:
            if self.flow_trend.RawMin >= 0:
                flow_data = struct.unpack("H" * 100, flow_trend_data.Data)
            else:
                flow_data = struct.unpack("h" * 100, flow_trend_data.Data)
            flow_data_mean = np.array([(sum(flow_data[i:i * window_size]) / window_size for i in range(100 // window_size))])
            return flow_data_mean, density_data_mean

    def _refresh_simulation_data(self, current_timestamp):
        sol = solve_ivp(self._deriv, [self.last_timestamp, current_timestamp], self.simulation_data)
        self.simulation_data = sol.y[:, -1] # noqa
        self.last_t = current_timestamp

    def _deriv(self, t: float, y: np.array):
        # print(t)
        # print(y)
        self.pipe_density_gradient = - np.diff(y, prepend=self.density_interp(t)) / self.lds_simulation.ResolutionMeters
        pipe_velocity = self.velocity_interp(t) / self.pipeline_area
        return pipe_velocity * self.pipe_density_gradient

    def calculate_velocity(self, flow_data: np.ndarray, density_data: np.ndarray) -> list:
        raise NotImplementedError
