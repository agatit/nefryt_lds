import logging
import math
import struct
from sqlalchemy import select, desc
from sqlalchemy.orm import Session
from database.models import lds
from db import get_engine
from simulator.simulations.base import SimulationBase
from simulator.simulations.utils import SimulatorData


class SimulationDensityBase(SimulationBase):
    def __init__(self, simulation: lds.Simulation, db_uri: str, trend: lds.Trend, unit: lds.Unit, plot_sim: bool = False):
        super().__init__(simulation, db_uri, plot_sim)
        self.flow_trend = trend
        self.flow_unit = unit
        try:
            self.pipeline_width = float(self.params['WIDTH'])
        except ValueError:
            raise ValueError(f'\'WIDTH\' param for simulation {self.lds_simulation.ID} must be a float')

    def calculate_simulation_data_on_start(self, current_timestamp: int):
        previous_distance = 0
        timestamp = current_timestamp - 1
        buffer_size = 100
        previous_flow = None
        previous_density = None

        iter_flow_trend = iter([])
        iter_density_trend = iter([])
        flow_trend_data = None
        density_trend_data = None

        while True:
            if flow_trend_data is None:
                statement = (select(lds.TrendData)
                            .where(lds.TrendData.TrendID == self.flow_trend.ID) # noqa
                            .where(lds.TrendData.Time <= timestamp)
                            .order_by(desc(lds.TrendData.Time)) # noqa
                            .limit(buffer_size))
                with Session(get_engine()) as session:
                    results_flow_trend = session.execute(statement).scalars().all()

                iter_flow_trend = iter(results_flow_trend)
                flow_trend_data = next(iter_flow_trend, None)
                if flow_trend_data is None:
                    logging.warning(f'Cannot simulate full data on start of simulation with id={self.lds_simulation.ID} '
                                    f'cause: not enough flow trend with id={self.flow_trend.ID} data')
                    break

            if self.flow_trend.RawMin >= 0:
                one_second_data = struct.unpack("H" * 100, flow_trend_data.Data)
            else:
                one_second_data = struct.unpack("h" * 100, flow_trend_data.Data)
            avg_past_flow = (sum(one_second_data) / len(one_second_data)) / float(self.flow_unit.Multiplier)
            if flow_trend_data.Time != timestamp and previous_flow is not None:
                delta_flow = (avg_past_flow - previous_flow[0]) / (previous_flow[1] - flow_trend_data.Time)
                avg_past_flow = previous_flow[0] + (previous_flow[1] - timestamp) * delta_flow
            elif flow_trend_data.Time == timestamp:
                previous_flow = (avg_past_flow, flow_trend_data.Time)
                flow_trend_data = next(iter_flow_trend, None)
            velocity = self.calculate_velocity(avg_past_flow, 0)

            if density_trend_data is None:
                statement = (select(lds.TrendData)
                            .where(lds.TrendData.TrendID == self.simulation_trend.ID)
                            .where(lds.TrendData.Time <= timestamp)
                            .order_by(desc(lds.TrendData.Time)) # noqa
                            .limit(buffer_size))
                with Session(get_engine()) as session:
                    results_density_trend = session.execute(statement).scalars().all()

                iter_density_trend = iter(results_density_trend)
                density_trend_data = next(iter_density_trend, None)
                if density_trend_data is None:
                    logging.warning(
                        f'Cannot simulate full data on start of simulation with id={self.lds_simulation.ID} '
                        f'cause: not enough density trend with id={self.simulation_trend.ID} data')
                    break

            if self.simulation_trend.RawMin >= 0:
                one_second_data = struct.unpack("H" * 100, density_trend_data.Data)
            else:
                one_second_data = struct.unpack("h" * 100, density_trend_data.Data)
            avg_past_density = (sum(one_second_data) / len(one_second_data)) / float(self.simulation_unit.Multiplier)
            density = None
            if density_trend_data.Time != timestamp and previous_density is not None:
                delta_density = (avg_past_density - previous_density[0]) / (previous_density[1] - density_trend_data.Time)
                density = previous_density[0] + (previous_density[1] - timestamp) * delta_density
            elif density_trend_data.Time == timestamp:
                density = avg_past_density
                previous_density = (avg_past_density, density_trend_data.Time)
                density_trend_data = next(iter_density_trend, None)

            previous_distance += velocity
            self.simulation_data.append(SimulatorData(Distance=previous_distance, Data=density))
            if previous_distance >= self.pipeline_length:
                break
            timestamp -= 1

    def calculate_simulation_data(self, current_timestamp: int):
        current_data = self._get_current_data(current_timestamp)
        if current_data:
            flow, density = current_data
            print(current_timestamp, flow, density)
            velocity = self.calculate_velocity(flow, density)
            self._refresh_simulation_data(velocity, density)

    def _get_current_data(self, current_timestamp: int):
        statement_flow = (select(lds.TrendData)
                         .where(lds.TrendData.TrendID == self.flow_trend.ID)  # noqa
                         .where(lds.TrendData.Time <= current_timestamp)
                         .order_by(desc(lds.TrendData.Time))  # noqa
                         .limit(1))
        statement_density = (select(lds.TrendData)
                            .where(lds.TrendData.TrendID == self.simulation_trend.ID) # noqa
                            .where(lds.TrendData.Time == current_timestamp)) # noqa

        with Session(get_engine()) as session:
            density_trend_data = session.execute(statement_density).scalars().first()
            flow_trend_data = session.execute(statement_flow).scalars().first()

        density = None
        if density_trend_data is not None:
            if self.simulation_trend.RawMin >= 0:
                one_second_data = struct.unpack("H" * 100, density_trend_data.Data)
            else:
                one_second_data = struct.unpack("h" * 100, density_trend_data.Data)
            density = (sum(one_second_data) / len(one_second_data)) / float(self.simulation_unit.Multiplier)

        if flow_trend_data is None:
            logging.warning(f'No flow trend data for simulation with id={self.lds_simulation.ID}')
            return None
        else:
            if self.flow_trend.RawMin >= 0:
                one_second_data = struct.unpack("H" * 100, flow_trend_data.Data)
            else:
                one_second_data = struct.unpack("h" * 100, flow_trend_data.Data)
            flow = (sum(one_second_data) / len(one_second_data)) / float(self.flow_unit.Multiplier)
            return flow, density

    def _refresh_simulation_data(self, velocity: float, density: float | None):
        self.simulation_data.insert(0, SimulatorData(Distance=0, Data=density))
        new_simulation_data_list = []
        for simulator_data in self.simulation_data:
            simulator_data.Distance += velocity
            new_simulation_data_list.append(simulator_data)
            if simulator_data.Distance >= self.pipeline_length:
                break
        self.simulation_data = new_simulation_data_list

    def calculate_velocity(self, flow: float, density: float) -> float:
        raise NotImplementedError


class SimulationDensityVolume(SimulationDensityBase):
    def calculate_velocity(self, flow: float, _) -> float:
        area = (self.pipeline_width/2)**2 * math.pi
        return flow / area


class SimulationDensityMass(SimulationDensityBase):
    def calculate_velocity(self, flow: float, density: float) -> float | None:
        area = (self.pipeline_width/2)**2 * math.pi
        return flow / (density * area)


def factory_simulation_density_object(simulation: lds.Simulation, db_uri: str) -> SimulationDensityBase:
    simulation_base = SimulationBase(simulation, db_uri)
    try:
        flow_trend_id = simulation_base.params['FLOW_TREND']
    except KeyError:
        raise ValueError(f'No param \'FLOW_TREND\' for simulation {simulation_base.lds_simulation.ID}')

    with Session(get_engine()) as session:
        flow_trend: lds.Trend | None = session.get(lds.Trend, flow_trend_id)
    if not flow_trend:
        raise ValueError(f'No trend with id = {flow_trend_id} for simulation {simulation_base.lds_simulation.ID}')

    with Session(get_engine()) as session:
        unit: lds.Unit | None = session.get(lds.Unit, flow_trend.UnitID)
    if not unit:
        raise ValueError(f'No unit with id = {flow_trend.UnitID} for trend with id = {flow_trend_id} '
                         f'for simulation {simulation_base.lds_simulation.ID}')


    if unit.BaseID.strip() == 'm3_s':
        return SimulationDensityVolume(simulation, db_uri, flow_trend, unit, plot_sim=True)
    elif unit.BaseID.strip() == 'kg_h':
        return SimulationDensityMass(simulation, db_uri, flow_trend, unit)
    else:
        raise ValueError(f'Wrong unit base for trend with id = {flow_trend_id} for simulation {simulation_base.lds_simulation.ID}')

