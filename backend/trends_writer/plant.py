import time
from sqlalchemy import select, literal
import numpy as np
import threading
from database import lds
from .db import global_session, Session
from .trend import TrendQuick


class PipePlant:
    def __init__(self):
        self.trends = []
        self.read_trends()

    def read_trends(self):
        stmt = select(lds.Trend) \
            .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID) \
            .where(lds.TrendDef.ID == literal('QUICK'))
        result = global_session.execute(stmt).fetchall()

        self.trends = [TrendQuick(trend[0].ID) for trend in result]

    def update(self, register, data):
        trend: TrendQuick
        for trend in self.trends:
            if trend.register == register:
                # TODO: async
                threading.Thread(target=trend.update, args=(np.array(data), round(time.time()), Session())).start()
