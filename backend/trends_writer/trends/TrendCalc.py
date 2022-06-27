import struct
from typing import List
import numpy as np
import logging
from datetime import datetime
from sqlalchemy import select

from database import lds
from ..db import session
from . import TrendBase
import time


class TrendCalc(TrendBase):

    def __init__(self, id: int, parent_id: int = None):
        super().__init__(id, parent_id)


    def update(self, data: List[int], timestamp: int, parent_id: int = None):
        logging.info(f"Trend {self.__class__.__name__} ({self.id}) precessing...")

        timestamp = int(time.time())
        calculated_data, diff_in_time = self.calculate(data, parent_id)
        if calculated_data and diff_in_time:
            timestamp = timestamp - diff_in_time
            super().update(calculated_data, timestamp, parent_id)


    def calculate(self, data, parent_id: int = None):
        raise NotImplementedError


    def initiate_buffer(self, parent_id: int = None):
        valid = []
        storage = np.array([])

        stmt = select([lds.TrendData]) \
            .where(lds.TrendData.TrendID == parent_id) \
            .order_by(lds.TrendData.Time.desc()) \
            .limit(2 * self.window_size)

        result = session.execute(stmt)
        recent_trend_data_list = result.fetchall()
        
        timestamp = recent_trend_data_list[0][0].Time
        # print(timestamp)
        newest_date_time = datetime.fromtimestamp(timestamp)
        # print(newest_date_time)

        for count, trend_data in enumerate(recent_trend_data_list):
            prev_date_time = datetime.fromtimestamp(
                trend_data[0].Time)
            diff = newest_date_time - prev_date_time
            diff_in_sec = diff.total_seconds()

            if diff_in_sec >= 0.98 and diff_in_sec <= 1.02 or diff_in_sec == 0: #WTF? Magic numbers?
                valid.append(count)
                newest_date_time = prev_date_time
            # else:
                # print(diff_in_sec)

        if(len(valid) != len(recent_trend_data_list)):
            max_value = max(valid)
            for _ in range(len(valid), len(recent_trend_data_list)):
                valid.append(max_value)
    
        for valid_count in reversed(valid):
            decoded = list(struct.unpack(
                '<100h', recent_trend_data_list[valid_count][0].Data))
            storage = np.append(
                storage, decoded)
        
        logging.info(f"Trend {self.__class__.__name__}={self.id} buffer read {len(storage)} values from {parent_id}")

        return storage

