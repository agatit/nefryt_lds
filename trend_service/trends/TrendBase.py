import logging
import struct
import time
from typing import List

from ..database import orm
from ..services import service_trend, service_trend_data


class FlyweightMeta(type):
    _objects = {}

    def __call__(cls, key, *args, **kwargs):
        if key in cls._objects:
            return cls._objects[key]
        else:
            obj = super().__call__(key, *args, **kwargs)
            cls._objects[key] = obj
            return obj


class TrendBase(metaclass=FlyweightMeta):

    def __init__(self, trend: orm.Trend):
        self.trend: orm.Trend = trend
        self.children: List[TrendBase] = []
        self.params = {}
        self.readParamsFromDB()

    def readParamsFromDB(self):
        self.params = service_trend.get_params_and_values(self.trend)

    def processData(self, data, parent_id: int = None):
        raise NotImplementedError

    def save(self, data, timestamp: int = None):
        try:
            if timestamp is None:
                timestamp = int(time.time())
            #  2 okna razy 100
            packed_data = struct.pack('<100h', *data)
            service_trend_data.insert(self.trend, packed_data, timestamp)
            logging.info(self.__class__.__name__ + ": data saved")
        except Exception as e:
            logging.exception(e)
            print(e)
