import sqlalchemy as sql
from sqlalchemy import and_

from ..database import *
from ..database import Session, engine, orm
from ..services import service_trend
from .TrendBase import TrendBase


class CalcTrend(TrendBase):

    def __init__(self, trend: orm.Trend):
        super().__init__(trend)

    def processData(self, data):
        pass

    def calculate(self):
        pass
