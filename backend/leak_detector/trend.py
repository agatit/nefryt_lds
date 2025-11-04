import logging
import struct
import numpy as np
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from database import lds
from db import get_engine


class Trend:
    def __init__(self, trend: lds.Trend):
        self.id = trend.ID
        self.lds_trend = trend
        self.node_id = trend.NodeID
        logging.debug(f"Trend {self.id} {self.node_id} created")

    def get_trend_data(self, begin: int, end: int, data_per_second: int = 100) -> np.ndarray:
        begin_ts = begin // 1000
        end_ts = end // 1000
        expected_data_length = (end_ts-begin_ts)*data_per_second
        if data_per_second != 100:
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

        next_idx = 99 - (begin//10)%100
        for db_data in db_data_list:
            while current_timestamp < db_data.Time:
                data_list += [last_valid] * data_per_second
                current_timestamp += 1

            if self.lds_trend.RawMin >= 0:
                one_second_data = struct.unpack("H" * 100, db_data.Data)
            else:
                one_second_data = struct.unpack("h" * 100, db_data.Data)

            for raw_value in one_second_data[next_idx::-100//data_per_second]:
                last_valid = (self.lds_trend.ScaledMax - self.lds_trend.ScaledMin) \
                             * (raw_value - self.lds_trend.RawMin) \
                             / (self.lds_trend.RawMax - self.lds_trend.RawMin) \
                             + self.lds_trend.ScaledMin
                if len(data_list) < expected_data_length:
                    data_list.append(last_valid)
                else:
                    break

            last_idx = next_idx % (100//data_per_second)
            next_idx = 100 - (100//data_per_second) + last_idx
            current_timestamp += 1
        if len(data_list) < expected_data_length:
            data_list.extend([last_valid] * ((end-begin)*data_per_second - len(data_list)))
        logging.debug(f"Got data successfully.")
        return np.array(data_list)
