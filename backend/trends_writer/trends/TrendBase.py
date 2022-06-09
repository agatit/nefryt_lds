from typing import List

from trends_writer import session
from database.models import lds
from ..services import service_trend


class TrendBase:
    def __init__(self, trend: lds.Trend):
        self.trend: lds.Trend = trend
        self.children: List[TrendBase] = []
        self.params = []
        self.readParamsFromDB()

    def readParamsFromDB(self):
        self.params = service_trend.get_params_and_values(self.trend)

    def processData(self):
        pass

    def save(self):
        pass
