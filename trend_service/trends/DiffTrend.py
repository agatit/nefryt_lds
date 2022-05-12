import sqlalchemy as sql
from sqlalchemy import and_

from ..database import *
from ..database import Session, engine, orm
from ..services import service_trend
from .CalcTrend import CalcTrend
from .TrendBase import TrendBase


class DiffTrend(CalcTrend):

    def __init__(self, trend: orm.Trend):
        super().__init__(trend)

    def calculate(self):
        pass
