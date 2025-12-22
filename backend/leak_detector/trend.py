import logging
import struct
import numpy as np
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from database import lds
from db import get_engine

logger = logging.getLogger(__name__)


class Trend:
    def __init__(self, trend: lds.Trend):
        self.id = trend.ID
        self.lds_trend = trend
        self.node_id = trend.NodeID
        self.block_size = 100
        logger.debug(f"Trend: Created with id = {self.id}")

    def get_trend_data(self, begin: int, end: int, min_wave_value: float = 0.0, data_per_second: int = 100) -> np.ndarray:
        begin_ts = begin // 1000
        end_ts = end // 1000
        expected_data_length = (end_ts-begin_ts)*data_per_second
        if data_per_second != self.block_size:
            expected_data_length += 1
        current_timestamp = begin
        last_valid = 0
        data_list = []

        statement = select(lds.TrendData) \
            .where(and_(lds.TrendData.Time >= begin_ts,
                        lds.TrendData.Time <= end_ts,
                        lds.TrendData.TrendID == self.id)) \
            .order_by(lds.TrendData.Time)
        with Session(get_engine()) as session:
            db_data_list = session.scalars(statement).all()

        next_idx = self.block_size - 1 - (begin//10)%self.block_size
        for db_data in db_data_list:
            while current_timestamp < db_data.Time:
                logger.debug(f'Trend: No data for trend with id = {self.id} in timestamp = {current_timestamp}')
                data_list += [last_valid] * data_per_second
                current_timestamp += 1

            if self.lds_trend.RawMin >= 0:
                one_second_data = struct.unpack("H" * self.block_size, db_data.Data)
            else:
                one_second_data = struct.unpack("h" * self.block_size, db_data.Data)

            for raw_value in one_second_data[next_idx::-self.block_size//data_per_second]:
                last_valid = (self.lds_trend.ScaledMax - self.lds_trend.ScaledMin) \
                             * (raw_value - self.lds_trend.RawMin) \
                             / (self.lds_trend.RawMax - self.lds_trend.RawMin) \
                             + self.lds_trend.ScaledMin
                last_valid = last_valid if abs(last_valid) > min_wave_value else 0
                if len(data_list) < expected_data_length:
                    data_list.append(last_valid)
                else:
                    break

            last_idx = next_idx % (self.block_size//data_per_second)
            next_idx = self.block_size - (self.block_size//data_per_second) + last_idx
            current_timestamp += 1
        if len(data_list) < expected_data_length:
            logger.debug(f'Trend: Extend trend data for trend with id = {self.id} by {(end_ts-begin_ts)*data_per_second - len(data_list)} elements')
            data_list.extend([last_valid] * ((end_ts-begin_ts)*data_per_second - len(data_list)))
        return np.array(data_list)
