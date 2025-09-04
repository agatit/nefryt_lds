import logging
import math
import struct
from typing import Callable
import numpy as np
from scipy.interpolate import interp1d, PchipInterpolator
from sqlalchemy import select, desc, and_
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
        self.pipeline_area = np.ones_like(self.simulation_data) * (pipeline_width/2)**2 * math.pi
        self.pipeline_area[len(self.simulation_data)//2:] *= 10
        self.previous_correct_density_time = 0
        self.window_size = 5
        self.max_flow_gap_in_seconds = 3
        self.density_interp = None
        self.flow_interp = None

    def calculate_simulation_data_on_start(self):
        volume_covered = 0
        default_buffer_size = 100
        last_timestamp = self.simulation_timestamp
        pipeline_volume = sum(self.pipeline_area * self.simulation_segment_length)
        first_calculated_timestamp = None
        flows = []
        densities = []

        while volume_covered < pipeline_volume and first_calculated_timestamp is None:
            buffer_size = default_buffer_size
            new_flows, buffer_size, first_calculated_timestamp = self._read_start_flow_data(last_timestamp, buffer_size)
            flows += new_flows.values()

            if len(new_flows) < buffer_size - 1:
                buffer_size = len(new_flows) + 1

            densities += self._read_start_density_data(last_timestamp, buffer_size)

            if buffer_size > 0:
                densities, new_buffer_size = self._fill_density_data(densities, last_timestamp, buffer_size)
                if new_buffer_size != buffer_size:
                    flows = flows[:len(densities)]
                    first_calculated_timestamp = last_timestamp - new_buffer_size - 1
                    break
                for i, (one_sec_flow_interp, one_sec_density) in enumerate(zip(flows[-buffer_size+1:], densities[-buffer_size+1:])):
                    timestamps = np.arange(last_timestamp - buffer_size + i + 1, last_timestamp - buffer_size + i + 2, 100)
                    one_sec_flow = one_sec_flow_interp(timestamps)
                    volume_covered += np.mean(one_sec_flow)

            last_timestamp -= buffer_size - 1

        first_calculated_timestamp = last_timestamp if not first_calculated_timestamp else first_calculated_timestamp
        for i, (flow, density) in enumerate(zip(reversed(flows), reversed(densities))):
            density_timestamps = np.linspace(first_calculated_timestamp + i, first_calculated_timestamp + i + 1, len(density))
            self.density_interp = interp1d(density_timestamps, density, kind='linear', fill_value='extrapolate')
            self.flow_interp = flow
            self._refresh_simulation_data(first_calculated_timestamp + i)

    def _read_start_flow_data(self, last_timestamp: int, buffer_size: int) -> (dict, int, int | None):
        first_calculated_timestamp = None
        mean_data_count = 10
        new_flows = {}
        statement_flow = (select(lds.TrendData)
                          .where(lds.TrendData.TrendID == self.flow_trend.ID)
                          .where(and_(lds.TrendData.Time <= last_timestamp, lds.TrendData.Time >= last_timestamp - buffer_size))
                          .order_by(desc(lds.TrendData.Time)))  # noqa

        with Session(get_engine()) as session:
            flow_data_pack = session.scalars(statement_flow).all()

        if len(flow_data_pack) <= 2 or flow_data_pack[0].Time != last_timestamp:
            first_calculated_timestamp = last_timestamp
            buffer_size = 0

        if buffer_size > 0:
            for prev_flow_data, next_flow_data in zip(flow_data_pack[2:], flow_data_pack):
                t_prev = prev_flow_data.Time
                t_next = next_flow_data.Time
                if t_next - t_prev > self.max_flow_gap_in_seconds + 1:
                    buffer_size = len(new_flows) + 1 if len(new_flows) != 0 else 0
                    first_calculated_timestamp = last_timestamp - len(new_flows)
                    break
                else:
                    if self.flow_trend.RawMin >= 0:
                        data_prev = struct.unpack("H" * 100, prev_flow_data.Data)
                        data_next = struct.unpack("H" * 100, next_flow_data.Data)
                    else:
                        data_prev = struct.unpack("h" * 100, prev_flow_data.Data)
                        data_next = struct.unpack("h" * 100, next_flow_data.Data)

                    mean_data_prev = (sum(data_prev[-mean_data_count:]) / mean_data_count) * float(self.flow_unit.Multiplier)
                    mean_data_next = (sum(data_next[:mean_data_count]) / mean_data_count) * float(self.flow_unit.Multiplier)
                    diff_t = t_next - t_prev - 1
                    diff_data = mean_data_next - mean_data_prev
                    for ts in range(t_prev + 1, t_next):
                        flow = lambda t, m=mean_data_prev, tp=t_prev, dt=diff_t, dd=diff_data: (
                                m + ((t - tp - 1) / dt) * dd)
                        new_flows[ts] = flow

        return new_flows, buffer_size, first_calculated_timestamp

    def _read_start_density_data(self, last_timestamp: int, buffer_size: int) -> list:
        densities = []
        statement_density = (((select(lds.TrendData)
                               .where(lds.TrendData.TrendID == self.simulation_trend.ID))
                              .where(and_(lds.TrendData.Time < last_timestamp, lds.TrendData.Time > last_timestamp - buffer_size)))
                             .order_by(desc(lds.TrendData.Time)))  # noqa

        with Session(get_engine()) as session:
            density_trend_pack = session.scalars(statement_density).all()

        density_data_iter = iter(density_trend_pack)
        density_data = next(density_data_iter, None)

        for i in range(buffer_size - 1):
            if density_data and density_data.Time >= last_timestamp - i - 1:
                if self.simulation_trend.RawMin >= 0:
                    data = struct.unpack("H" * 100, density_data.Data)
                else:
                    data = struct.unpack("h" * 100, density_data.Data)
                data = [(sum(data[i * self.window_size:(i + 1) * self.window_size]) / self.window_size)
                        * float(self.simulation_unit.Multiplier) for i in range(100 // self.window_size)]
                densities.append(data)
                density_data = next(density_data_iter, None)
            else:
                densities.append(None)

        return densities

    def _fill_density_data(self, densities: list, last_timestamp: int, buffer_size: int):
        if densities[-1] is None:
            statement_density = (((select(lds.TrendData)
                                   .where(lds.TrendData.TrendID == self.simulation_trend.ID))
                                  .where(lds.TrendData.Time <= last_timestamp - buffer_size)) # noqa
                                 .order_by(desc(lds.TrendData.Time)) # noqa
                                 .limit(1))

            with Session(get_engine()) as session:
                prev_density_trend_data = session.execute(statement_density).scalars().first()

            if prev_density_trend_data:
                if self.simulation_trend.RawMin >= 0:
                    prev_data = struct.unpack("H" * 100, prev_density_trend_data.Data)
                else:
                    prev_data = struct.unpack("h" * 100, prev_density_trend_data.Data)

                prev_data = [(sum(prev_data[i * self.window_size:(i + 1) * self.window_size]) / self.window_size)
                             * float(self.simulation_unit.Multiplier) for i in range(100 // self.window_size)][-1]
                prev_t = prev_density_trend_data.Time + 1 - (1 / (100 // self.window_size))
                last_not_none_idx = next((len(densities) - i for i, j in enumerate(reversed(densities), 1) if j is not None), None)
                if last_not_none_idx is None:
                    densities = densities[:-buffer_size]
                    buffer_size = 0
                    return densities, buffer_size
                next_data = densities[last_not_none_idx][0]
                next_t = self.simulation_timestamp - last_not_none_idx - 1
                diff_t = next_t - prev_t
                curr_t = self.simulation_timestamp - len(densities)
                densities[-1] = [prev_data + ((curr_t + diff * (1 / (100 // self.window_size)) - prev_t) / diff_t)
                                 * (next_data - prev_data) for diff in range(100 // self.window_size)]
            else:
                last_not_none_idx = next((len(densities) - i for i, j in enumerate(reversed(densities), 1) if j is not None), None)
                if last_not_none_idx is None:
                    densities = densities[:-buffer_size+1]
                    buffer_size = 0
                    return densities, buffer_size
                else:
                    buffer_size -= (len(densities) - last_not_none_idx)
                    densities = densities[:last_not_none_idx+1]

        if densities[0] is None:
            first_density = next((density for density in densities if density is not None))
            for i in range(len(densities)):
                if densities[i]:
                    break
                else:
                    densities[i] = [first_density[-1]] * (100 // self.window_size)

        i = len(densities) - buffer_size + 1
        while i < len(densities):
            if densities[i] is None:
                j = i+1
                while j < len(densities) and densities[j] is None:
                    j += 1

                prev_data = densities[-buffer_size + i][-1]
                prev_t = i
                next_data = densities[-buffer_size + j + 1][0]
                next_t = j
                diff_t = next_t - prev_t

                for curr_t in range(i, j):
                    densities[curr_t] = [prev_data + ((curr_t + diff * (1 / (100 // self.window_size)) - prev_t) / diff_t)
                                         * (next_data - prev_data) for diff in range(100 // self.window_size)]

                i = j
            else:
                i += 1

        return densities, buffer_size

    def calculate_simulation_data(self):
        density_data = self._get_current_density_data()
        if density_data is not None:
            self.flow_interp = self._get_current_flow_data()

            if self.flow_interp:
                density_timestamps = np.linspace(self.simulation_timestamp, self.simulation_timestamp + 1, len(density_data))
                self.density_interp = interp1d(density_timestamps, density_data, kind='linear', fill_value='extrapolate')
                self._refresh_simulation_data(self.simulation_timestamp)

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
                    last_density = ((sum(density_data[-(window+1)*window_size:-(window*window_size+1)])/window_size)
                                    * float(self.simulation_unit.Multiplier))

                last_density = last_density if last_density > 0 else \
                    (float(self.density_interp(self.simulation_timestamp)) if self.density_interp is not None else 1)
                return [last_density] * (100 // window_size)

            density_data = [(sum(density_data[i*window_size:(i+1)*window_size])/window_size)
                            * float(self.simulation_unit.Multiplier) for i in range(100//window_size)]
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
        elif (self.simulation_timestamp - data_prev.Time - 1) > self.max_flow_gap_in_seconds:
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
            mean_data_prev = (sum(data_prev[-mean_data_count:]) / mean_data_count) * float(self.flow_unit.Multiplier)
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

            mean_data_prev = (sum(data_prev[-mean_data_count:]) / mean_data_count) * float(self.flow_unit.Multiplier)
            if mean_data_prev < 0:
                logging.warning(f'Simulation {self.lds_simulation.ID} flow previous data have incorrect values'
                                f'(should not be < 0, replacing this value with zero flow)')
                mean_data_prev = 0
            mean_data_next = (sum(data_next[:mean_data_count]) / mean_data_count) * float(self.flow_unit.Multiplier)
            if mean_data_next < 0:
                logging.warning(f'Simulation {self.lds_simulation.ID} flow next data have incorrect values'
                                f'(should not be < 0, replacing this value with zero flow)')
                mean_data_next = 0
            diff_t = t_next - t_prev - 1
            diff_data = mean_data_next - mean_data_prev

            return lambda t: mean_data_prev + ((t - t_prev - 1) / diff_t) * diff_data

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
            velocity = self.calculate_velocity(flow_in_step, [])
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

    def calculate_velocity(self, flow_data: np.ndarray, density_data: list) -> np.ndarray:
        raise NotImplementedError
