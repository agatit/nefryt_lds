import sqlalchemy as sql
from sqlalchemy import and_

from ..database import *
from ..database import Session, engine, orm
from .TrendBase import TrendBase
from ..services import service_trend

class QuickTrend(TrendBase):

    def __init__(self, trend: orm.Trend):
        super().__init__(trend)
        
    def processData(self):
        pass

    def save(self):
        pass
