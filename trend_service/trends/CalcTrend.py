from .TrendBase import TrendBase


class CalcTrend(TrendBase):

    def __init__(self, trend_ID):
        super().__init__(trend_ID)

    def readParamsFromDB(self):
        pass

    def processData(self):
        pass

    def save(self):
        pass

    def calculate(self):
        pass
