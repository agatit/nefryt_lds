import time
from sqlalchemy import select, and_
import numpy as np

from database import lds
from .db import session
from .trends import TrendQuick

class PipePlant:
    __list = []

    def __init__(self):
        self.trends = []
        self.read_trends()

    def read_trends(self):

        # pobranie wszystkich trendow "QUICK"
        stmt = select([lds.Trend]) \
            .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID) \
            .where(lds.TrendDef.ID == 'QUICK')        
        result = session.execute(stmt).fetchall()

        self.trends = []
        for trend in result:
            quickTrend = TrendQuick(trend[0].ID)
            self.trends.append(quickTrend)

    def update(self, register, data):
        trend: TrendQuick
        for trend in self.trends:
            if trend.register == register:
                trend.update(np.array(data), int(time.time()))

pipe_plant = PipePlant()