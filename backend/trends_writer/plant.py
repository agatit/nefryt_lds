import atexit
import logging
import time
from sqlalchemy import select, literal
import numpy as np
import threading
from sqlalchemy.orm import Session
from database import lds
from .db import get_engine
from .profiler import Profiler
from .trend import TrendQuick


class PipePlant:
    def __init__(self, pool, use_asyncio=False, use_profiler=False):
        self.trends = []
        self.read_trends()
        self.use_profiler = use_profiler
        self.use_asyncio = use_asyncio
        self.pool = pool
        atexit.register(self.shutdown_pool)

    def read_trends(self):
        stmt = (select(lds.Trend)
                .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID)  # noqa
                .where(lds.TrendDef.ID == literal('QUICK')))
        with Session(get_engine()) as session:
            result = session.execute(stmt).fetchall()

        self.trends = [TrendQuick(trend[0].ID) for trend in result]

    def update(self, register, data):
        trend: TrendQuick
        for trend in self.trends:
            if trend.register == register:
                if self.use_asyncio:
                    if self.use_profiler:
                        timestamp = round(time.time())
                        Profiler.add_update(timestamp)
                        self.pool.apply_async(trend.update, args=(np.array(data), timestamp), callback=return_callback, error_callback=error_callback)
                    else:
                        self.pool.apply_async(trend.update, args=(np.array(data), round(time.time())), callback=return_callback, error_callback=error_callback)
                else:
                    if self.use_profiler:
                        threading.Thread(target=update_with_callback, args=(trend, data)).start()
                    else:
                        threading.Thread(target=trend.update, args=(np.array(data), round(time.time()))).start()

    def shutdown_pool(self):
        self.pool.close()
        self.pool.join()


def update_with_callback(trend, data):
    timestamp = round(time.time())
    Profiler.add_update(timestamp)
    trend.update(np.array(data), timestamp)
    Profiler.remove_update(timestamp)

def return_callback(timestamp):
    Profiler.remove_update(timestamp)

def error_callback(e):
    logging.error(f'Error in trend update process: {e}')
