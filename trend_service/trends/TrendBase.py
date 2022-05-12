import struct
import time
from typing import List

from ..database import *
from ..database import Session, engine, orm
from ..services import service_trend, service_trend_data


class TrendBase:
    def __init__(self, trend: orm.Trend):
        self.trend: orm.Trend = trend
        self.children: List[TrendBase] = []
        self.params = {}
        self.readParamsFromDB()

    def readParamsFromDB(self):
        self.params = service_trend.get_params_and_values(self.trend)

    def processData(self, data):
        pass

    def save(self, data):
        try:
            packed_data = struct.pack('<100h', *data)
            now = int(time.time() * 1000)
            service_trend_data.insert(self.trend, packed_data, now)
        except Exception as e:
            print(e)
