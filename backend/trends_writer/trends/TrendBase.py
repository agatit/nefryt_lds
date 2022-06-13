import logging
import struct
import time
from typing import List

from sqlalchemy import select, and_

from trends_writer import session
from database import lds
from ..services import service_trend, service_trend_data


class IndexedSingleton(type):
    _objects = {}

    def __call__(cls, key, *args, **kwargs):
        if key in cls._objects:
            return cls._objects[key]
        else:
            obj = super().__call__(key, *args, **kwargs)
            cls._objects[key] = obj
            return obj


class TrendBase(metaclass=IndexedSingleton):

    def __init__(self, trend: lds.Trend):
        self.trend: lds.Trend = trend
        self.children: List[TrendBase] = []
        self.params = {}
        self.readParamsFromDB()


    def readParamsFromDB(self):
        stmt = select([lds.TrendParamDef, lds.TrendParam]) \
            .select_from(lds.Trend) \
            .join(lds.TrendDef, lds.Trend.TrendDefID == lds.TrendDef.ID) \
            .join(lds.TrendParamDef, lds.TrendDef.ID == lds.TrendParamDef.TrendDefID) \
            .join(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID, lds.Trend.ID == lds.TrendParam.TrendID)) \
            .where(lds.Trend.ID == self.trend.ID)
        results = session.execute(stmt).fetchall()

        self.params = {}
        for tpd, tp in results:
            self.params[tpd.ID.strip()] = tp.Value


    def processData(self, data, parent_id: int = None):
        raise NotImplementedError


    def save(self, data, timestamp: int = None):
        try:
            if timestamp is None:
                timestamp = int(time.time())
            packed_data = struct.pack('<100h', *data)
            service_trend_data.insert(self.trend, packed_data, timestamp)
            logging.info(self.__class__.__name__ + ": data saved")
        except Exception as e:
            logging.exception(e)
            print(e)
