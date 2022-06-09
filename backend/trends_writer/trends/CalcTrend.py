from .TrendBase import TrendBase
from trends_writer import session
from database.models import lds


class CalcTrend(TrendBase):

    def __init__(self, trend: lds.Trend):
        super().__init__(trend)

    def readParamsFromDB(self):
        pass

    def processData(self):
        pass

    def save(self):
        pass

    def calculate(self):
        pass
