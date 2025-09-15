from datetime import datetime
import logging
from typing import List
import struct

from alembic.command import current
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import current_timestamp

from database import lds
from db import get_engine


class Trend:
    def __init__(self, trend: lds.Trend):
        self.id = trend.ID
        self.lds_trend = trend
        self.node_id = trend.NodeID
        logging.debug(f"Trend {self.id} {self.node_id} created")

    def get_trend_data(self, begin: int, end: int) -> List[float]:
        begin = begin // 1000
        end = end // 1000
        # logging.info(f"Get data from {begin} to {end} in trend {self.id}")
        current_timestamp = begin
        # reading trends definitions neccessary for scaling

        last_valid = 0 # ostatnia prawidłowa wartość - do wypełniania pól z wartościami nieprawidływmi
    
        data_list = []

        # for every chunk
        statement = select(lds.TrendData) \
                .where(and_(lds.TrendData.Time >= begin,
                            lds.TrendData.Time < end,
                            lds.TrendData.TrendID == self.id)) \
                .order_by(lds.TrendData.Time)
        with Session(get_engine()) as session:
            trend_datas = session.scalars(statement).all()

        for db_data in trend_datas:
            while current_timestamp < db_data.Time:
                data_list += [last_valid] * 100
                current_timestamp += 1

            if self.lds_trend.RawMin >= 0:
                one_second_data = struct.unpack("H" * 100, db_data.Data)
            else:
                one_second_data = struct.unpack("h" * 100, db_data.Data)

            for raw_value in one_second_data:
                last_valid = (self.lds_trend.ScaledMax - self.lds_trend.ScaledMin) \
                             * (raw_value - self.lds_trend.RawMin) \
                             / (self.lds_trend.RawMax - self.lds_trend.RawMin) \
                             + self.lds_trend.ScaledMin
                data_list.append(last_valid)

            current_timestamp += 1

        if len(data_list) < (end-begin)*1000:
            data_list.extend([last_valid] * ((end-begin)*1000 - len(data_list)))
        logging.debug(f"Got data successfully.")
        return data_list
