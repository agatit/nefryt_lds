import time
from sqlalchemy import select, and_
import numpy as np
import threading

from database import lds
from .db import global_session, Session
from .trend import TrendQuick

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
        result = global_session.execute(stmt).fetchall()

        self.trends = []
        for trend in result:
            quickTrend = TrendQuick(trend[0].ID)
            self.trends.append(quickTrend)

    def update(self, register, data):
        trend: TrendQuick
        for trend in self.trends:
            if trend.register == register:
                # trend.update(np.array(data), round(time.time()))
                threading.Thread(target=trend.update, args=(np.array(data), round(time.time()), Session() )).start()