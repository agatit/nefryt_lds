import sqlalchemy as sql
from sqlalchemy import and_

from trends_writer import session
from database.models import lds
from .TrendBase import TrendBase
from ..services import service_trend

class QuickTrend(TrendBase):

    def __init__(self, trend: lds.Trend):
        super().__init__(trend)
        
    def processData(self):
        pass

    def save(self):
        pass
