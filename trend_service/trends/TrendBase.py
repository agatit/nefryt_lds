from typing import List

from ..database import *
from ..database import Session, engine, orm
from ..services import service_trend


class TrendBase:
    def __init__(self, trend: orm.Trend):
        self.trend: orm.Trend = trend
        self.children: List[TrendBase] = []
        self.params = []
        self.readParamsFromDB()

    def readParamsFromDB(self):
        self.params = service_trend.get_params_and_values(self.trend)

    def processData(self):
        pass

    def save(self):
        pass
