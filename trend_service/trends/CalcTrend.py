import logging

from ..database import orm
from .TrendBase import TrendBase


class CalcTrend(TrendBase):

    def __init__(self, trend: orm.Trend):
        super().__init__(trend)

    def processData(self, data, parent_id: int = None):
        try:
            result = self.calculate(data, parent_id)
            if result is not None:
                self.save(result)
        except Exception as e:
            raise e

    def calculate(self, data, parent_id: int = None):
        raise NotImplementedError
