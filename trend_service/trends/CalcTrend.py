from .TrendBase import TrendBase
from ..database import *


class CalcTrend(TrendBase):

    def __init__(self, trend: orm.Trend):
        super().__init__(trend)

    def readParamsFromDB(self):
        pass

    def processData(self):
        pass

    def save(self):
        pass

    def calculate(self):
        pass
