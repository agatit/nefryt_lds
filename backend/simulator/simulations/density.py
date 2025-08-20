import logging
import math
import struct
from typing import Callable
import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from database.models import lds
from db import get_engine
from simulator.simulations.base import SimulationBase


class SimulationDensityBase(SimulationBase):
    def __init__(self, simulation: lds.Simulation, db_uri: str = None):
        super().__init__(simulation, db_uri)

        try:
            pipeline_width = float(self.params['WIDTH'])
        except KeyError:
            raise ValueError(f'No \'WIDTH\' param for simulation {self.lds_simulation.ID}')
        except ValueError:
            raise ValueError(f'\'WIDTH\' param for simulation {self.lds_simulation.ID} must be a float')
        self.pipeline_area = (pipeline_width/2)**2 * math.pi
        self.previous_correct_density_time = 0
        self.density_interp = None
        self.velocity_interp = None
        self.flow_data = None

    def calculate_simulation_data_on_start(self):
        # TODO: load data on start if possible
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

    def calculate_simulation_data(self):
        density_data = self._get_current_density_data()
        if density_data is not None:
            flow_data_linear_interp = self._get_current_flow_data()

            if flow_data_linear_interp:
                flow_timestamps = np.arange(self.simulation_timestamp, self.simulation_timestamp + 1, 0.01)
                flow_data = flow_data_linear_interp(flow_timestamps)
                density_timestamps = np.linspace(self.simulation_timestamp, self.simulation_timestamp + 1, len(density_data))
                self.density_interp = interp1d(density_timestamps, density_data, kind='linear', fill_value='extrapolate')
                velocity_data = self.calculate_velocity(flow_data, density_data)
                self.velocity_interp = interp1d(flow_timestamps, velocity_data, kind='linear', fill_value='extrapolate')
                self._refresh_simulation_data()


    def _get_current_density_data(self) -> list | None:
        window_size = 5
        statement_density = (((select(lds.TrendData)
                             .where(lds.TrendData.TrendID == self.simulation_trend.ID))
                             .where(lds.TrendData.Time <= self.simulation_timestamp))
                             .order_by(desc(lds.TrendData.Time)) # noqa
                             .limit(1))

        with Session(get_engine()) as session:
            density_trend_data = session.execute(statement_density).scalars().first()

        if density_trend_data is not None:
            if self.simulation_trend.RawMin >= 0:
                density_data = struct.unpack("H" * 100, density_trend_data.Data)
            else:
                density_data = struct.unpack("h" * 100, density_trend_data.Data)
            if density_trend_data.Time != self.simulation_timestamp:
                logging.warning(f'Simulation {self.lds_simulation.ID} density data read incorrect timestamp '
                                f'(expected: {self.simulation_timestamp}, real: {density_trend_data.Time})')
                last_density = -1
                window = 0
                while last_density < 0 and (window + 1)*window_size <= 100:
                    last_density = sum(density_data[-(window+1)*window_size:-(window*window_size+1)])/window_size

                last_density = last_density if last_density > 0 else \
                    (float(self.density_interp(self.simulation_timestamp)) if self.density_interp is not None else 1)
                return [last_density] * (100 // window_size)

            density_data = [sum(density_data[i*window_size:(i+1)*window_size])/window_size for i in range(100//window_size)]
            if min(density_data) <= 0:
                logging.warning(f'Simulation {self.lds_simulation.ID} density data have incorrect values'
                                f'(should not be <= 0, replacing those values with last values)')
                last_density = float(self.density_interp(self.previous_correct_density_time)) if self.density_interp is not None else 1
                density_data = [data if data > 0 else last_density for data in density_data]

            self.previous_correct_density_time = self.simulation_timestamp
            return density_data
        elif self.density_interp is not None:
            logging.warning(f'No density trend data in database for simulation with id = {self.lds_simulation.ID}, '
                            f'timestamp {self.simulation_timestamp}, using saved density data')
            last_density = float(self.density_interp(self.previous_correct_density_time))
            return [last_density] * (100//window_size)
        else:
            logging.warning(f'No density trend data in database for simulation with id = {self.lds_simulation.ID}, '
                            f'timestamp {self.simulation_timestamp}, no new simulation data will be saved')
            return None

    def _get_current_flow_data(self) -> Callable | None:
        mean_data_count = 10
        max_time_gap = 3
        statement_prev = (select(lds.TrendData)
                           .where(lds.TrendData.TrendID == self.flow_trend.ID)  # noqa
                           .where(lds.TrendData.Time < self.simulation_timestamp)  # noqa
                           .order_by(desc(lds.TrendData.Time))  # noqa
                           .limit(1))
        statement_next = (select(lds.TrendData)
                           .where(lds.TrendData.TrendID == self.flow_trend.ID)  # noqa
                           .where(lds.TrendData.Time > self.simulation_timestamp)  # noqa
                           .limit(1))

        with Session(get_engine()) as session:
            data_prev = session.execute(statement_prev).scalars().first()
            data_next = session.execute(statement_next).scalars().first()

        if data_prev is None:
            logging.warning(f'No previous flow trend data for simulation with id={self.lds_simulation.ID},'
                            f'timestamp {self.simulation_timestamp}, no new simulation data will be saved')
            return None
        elif (self.simulation_timestamp - data_prev.Time - 1) > max_time_gap:
            if self.simulation_timestamp - data_prev.Time - 1 == self.previous_timestamp_diff:
                logging.warning(f'Timestamp difference between Trends Writer and Simulation modules, '
                                f'no new simulation data will be saved until timestamps are within maximum time gap'
                                f'(current gap: {self.simulation_timestamp - data_prev.Time - 1} seconds)')
            else:
                self.previous_timestamp_diff = self.simulation_timestamp - data_prev.Time - 1
            logging.warning(f'Previous flow trend data not in maximum time gap, '
                            f'(expected: {self.simulation_timestamp-1}, real: {data_prev.Time}),'
                            f' no new simulation data will be saved')
            return None
        elif data_next is None:
            logging.warning(f'No next flow trend data for simulation with id={self.lds_simulation.ID} '
                            f'timestamp {self.simulation_timestamp}, using only previous data')
            if self.flow_trend.RawMin >= 0:
                data_prev = struct.unpack("H" * 100, data_prev.Data)
            else:
                data_prev = struct.unpack("h" * 100, data_prev.Data)
            mean_data_prev = sum(data_prev[-mean_data_count:]) / mean_data_count
            return lambda t: np.ones_like(t) * (mean_data_prev if mean_data_prev > 0 else 0)
        else:
            t_prev = data_prev.Time
            t_next = data_next.Time
            if self.flow_trend.RawMin >= 0:
                data_prev = struct.unpack("H" * 100, data_prev.Data)
                data_next = struct.unpack("H" * 100, data_next.Data)
            else:
                data_prev = struct.unpack("h" * 100, data_prev.Data)
                data_next = struct.unpack("h" * 100, data_next.Data)

            mean_data_prev = sum(data_prev[-mean_data_count:]) / mean_data_count
            if mean_data_prev < 0:
                logging.warning(f'Simulation {self.lds_simulation.ID} flow previous data have incorrect values'
                                f'(should not be < 0, replacing this value with zero flow)')
                mean_data_prev = 0
            mean_data_next = sum(data_next[:mean_data_count]) / mean_data_count
            if mean_data_next < 0:
                logging.warning(f'Simulation {self.lds_simulation.ID} flow next data have incorrect values'
                                f'(should not be < 0, replacing this value with zero flow)')
                mean_data_next = 0
            diff_t = t_next - t_prev - 1
            diff_data = mean_data_next - mean_data_prev

            return lambda t: mean_data_prev + ((t - t_prev - 1) / diff_t) * diff_data

    def _refresh_simulation_data(self):
        sol = solve_ivp(fun=self._deriv, t_span=[self.simulation_timestamp, self.simulation_timestamp + 1], y0=self.simulation_data)
        self.simulation_data = sol.y[:, -1] # noqa

    def _deriv(self, t: float, y: np.array):
        self.pipe_density_gradient = - np.diff(y, prepend=self.density_interp(t)) / self.lds_simulation.ResolutionMeters
        pipe_velocity = self.velocity_interp(t) / self.pipeline_area
        return pipe_velocity * self.pipe_density_gradient

    def calculate_velocity(self, flow_data: np.ndarray, density_data: list) -> list:
        raise NotImplementedError
