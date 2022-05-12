import sqlalchemy as sql
from sqlalchemy import and_

from ..database import *
from ..database import Session, engine, orm
from ..services import service_trend
from .TrendBase import TrendBase


class QuickTrend(TrendBase):

    def __init__(self, trend: orm.Trend):
        super().__init__(trend)

    def processData(self, data):
        for child in self.children:
            child.processData(data)
        pass
