import logging
import math
import struct
import time

import numpy as np
from sqlalchemy import select, and_, literal
from sqlalchemy.orm import Session

from database.models import lds
from db import get_engine
from simulator.simulations.base import SimulationBase


class SimulationDensityBase(SimulationBase):
    def __init__(self, simulation: lds.Simulation, db_uri: str, trend: lds.Trend, unit: lds.Unit):
        super().__init__(simulation, db_uri)
        self.flow_trend = trend
        self.unit = unit
        self.pipeline_width = self.params['WIDTH']
        self.previous_flow = None
        self.buffer_resolution = self._set_resolution()
        self.buffer: list[float | None] = [None for _ in range(0, self.simulation_length, self.buffer_resolution)]
        self.ema = 0.0

    def _set_resolution(self):
        if int(self.simulation_length) < 500:
            return 1
        elif int(self.simulation_length) < 500*10:
            return int(self.simulation_length/500) if int(self.simulation_length/500) < self.simulation_resolution else self.simulation_resolution
        else:
            return 10 if self.simulation_resolution > 10 else self.simulation_resolution

    def calculate_simulation_data(self):
        velocity = self.calculate_velocity()
        refreshed_buffer = self._refresh_buffer_data(velocity)


        self.buffer = refreshed_buffer

    def _refresh_buffer_data(self, velocity: float) -> list[float | None]:
        new_buffer: list[None | float] = [None for _ in range(0, self.simulation_length, self.buffer_resolution)]
        for idx, (density1, density2) in enumerate(zip(self.buffer[:-1], self.buffer[1:])):
            distance = idx * self.buffer_resolution
            new_distance = distance + velocity * self.refresh_time
            new_distance_rounded = int(math.ceil(new_distance / self.buffer_resolution) * self.buffer_resolution)
            if new_distance_rounded > self.simulation_length:
                break
            pos = new_distance_rounded // self.buffer_resolution
            if density1 is None and density2 is None:
                new_buffer[pos] = None
            elif density1 is None:
                new_buffer[pos] = density2
            elif density2 is None:
                new_buffer[pos] = density1
            else:
                new_buffer[pos] = (((1 - (abs(new_distance_rounded - new_distance) / self.buffer_resolution)) * density1)
                            + ((1 - (abs(new_distance_rounded - new_distance + self.buffer_resolution) / self.buffer_resolution)) * density2))

        return new_buffer

    def calculate_velocity(self) -> float:
        raise NotImplementedError

    def read_flow_trend_previous_data(self) -> float | None:
        current_timestamp = int(time.time()) - 1
        statement = (select(lds.TrendData)
                     .where(and_(lds.TrendData.TrendID == literal(self.flow_trend.ID),
                                 lds.TrendData.Time > current_timestamp-self.refresh_time,
                                 lds.TrendData.Time <= current_timestamp)))

        with Session(get_engine()) as session:
            trend_datas = session.execute(statement).all()

        flow_sum = 0
        flow_data_count = 0
        for lds_data in trend_datas:
            if self.flow_trend.RawMin >= 0:
                one_second_data = struct.unpack("H" * 100, lds_data.Data)
            else:
                one_second_data = struct.unpack("h" * 100, lds_data.Data)

            one_second_data = list(filter(None, one_second_data))
            flow_sum += sum(one_second_data)
            flow_data_count += len(one_second_data)

        if flow_data_count == 0:
            logging.warning(f'Cannot calculate average flow for trend {self.flow_trend.ID} in simulation {self.id}')
            return None
        avg_flow = flow_sum / flow_data_count
        return avg_flow / self.unit.Multiplier

    def read_density_trend_data(self, new_data_count: int, velocity: float):
        time_deltas = [(i*self.buffer_resolution) / velocity for i in range(new_data_count)]
        current_timestamp = int(time.time()) - 1
        statement = (select(lds.TrendData)
                     .where(and_(lds.TrendData.TrendID == literal(self.simulation_trend_id),
                                 lds.TrendData.Time > current_timestamp - self.refresh_time,
                                 lds.TrendData.Time <= current_timestamp)))

        with Session(get_engine()) as session:
            trend_datas = session.execute(statement).all()

        if len(trend_datas) == 0:
            logging.warning(f'No density data for trend {self.simulation_trend_id} in simulation {self.id}')
            return None

        one_second_datas = []
        iter_trend_datas = iter(trend_datas)
        lds_data = next(iter_trend_datas, None)
        for timestamp in range(current_timestamp - self.refresh_time+1, current_timestamp+1):
            if lds_data is not None and lds_data.Time == timestamp:
                one_second_datas += list(struct.unpack("H" * 100, lds_data.Data))
                lds_data = next(iter_trend_datas, None)
            else:
                one_second_datas.append([None] * 100)




class SimulationDensityVolume(SimulationDensityBase):
    def calculate_velocity(self) -> float | None:
        avg_flow = self.read_flow_trend_previous_data()
        if avg_flow is None:
            return None
        if self.previous_flow:
            self.previous_flow = self.previous_flow * self.ema + (1 - self.ema) * avg_flow
        else:
            self.previous_flow = avg_flow
        area = (self.pipeline_width/2)**2 * math.pi
        return avg_flow / area



class SimulationDensityMass(SimulationDensityBase):
    pass



def create_simulation_density_object(simulation: lds.Simulation, db_uri: str) -> SimulationDensityBase:
    simulation_base = SimulationBase(simulation, db_uri)
    try:
        flow_trend_id = simulation_base.params['FLOW_TREND']
    except KeyError:
        raise ValueError(f'No param \'FLOW_TREND\' for simulation {simulation_base.id}')

    with Session(get_engine()) as session:
        flow_trend: lds.Trend | None = session.get(lds.Trend, flow_trend_id)
    if not flow_trend:
        raise ValueError(f'No trend with id = {flow_trend_id} for simulation {simulation_base.id}')

    with Session(get_engine()) as session:
        unit: lds.Unit | None = session.get(lds.Unit, flow_trend.UnitID)
    if not unit:
        raise ValueError(f'No unit with id = {flow_trend.UnitID} for trend with id = {flow_trend_id} '
                         f'for simulation {simulation_base.id}')

    if unit.BaseID.strip() == 'kg_h':
        return SimulationDensityVolume(simulation, db_uri, flow_trend, unit)
    elif unit.BaseID.strip() == 'm3_s':
        return SimulationDensityMass(simulation, db_uri, flow_trend, unit)
    else:
        raise ValueError(f'Wrong unit base for trend with id = {flow_trend_id} for simulation {simulation_base.id}')
