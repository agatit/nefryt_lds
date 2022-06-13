import struct

import numpy as np

from database import lds
from ..services import service_trend_data
from .TrendBase import TrendBase
import time


class CalcTrend(TrendBase):

    def __init__(self, trend: lds.Trend, parent_id: int = None):
        super().__init__(trend)

        self.output_size = 100

    def processData(self, data, parent_id: int = None):
        try:
            timestamp = int(time.time())
            result = self.calculate(data, parent_id)
            if result is not None and result[0] is not None:
                calculated_data, diff_in_time = result
                timestamp = timestamp - diff_in_time
                self.save(calculated_data, timestamp)
        except Exception as e:
            print(e)
            raise e

    def calculate(self, data, parent_id: int = None):
        raise NotImplementedError

    def initalizate_storage_with_recent_trend_data(self, parent_id: int = None):
        try:
            valid = []
            recent_trend_data_list = service_trend_data.get(
                parent_id, 2 * self.window_size)

            from datetime import datetime
            timestamp = recent_trend_data_list[0][0].Time
            # print(timestamp)
            newest_date_time = datetime.fromtimestamp(timestamp)
            # print(newest_date_time)

            for count, trend_data in enumerate(recent_trend_data_list):
                prev_date_time = datetime.fromtimestamp(
                    trend_data[0].Time)
                diff = newest_date_time - prev_date_time
                diff_in_sec = diff.total_seconds()

                if diff_in_sec >= 0.98 and diff_in_sec <= 1.02 or diff_in_sec == 0:
                    valid.append(count)
                    newest_date_time = prev_date_time
                # else:
                    # print(diff_in_sec)

            if(len(valid) != len(recent_trend_data_list)):
                max_value = max(valid)
                for _ in range(len(valid), len(recent_trend_data_list)):
                    valid.append(max_value)

            valid.reverse()

            for valid_count in valid:
                decoded = list(struct.unpack(
                    '<100h', recent_trend_data_list[valid_count][0].Data))
                self.storage = np.append(
                    self.storage, decoded)
        except Exception as e:
            raise e
