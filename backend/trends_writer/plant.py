import atexit
import logging
import sys
import time
from multiprocessing import Queue
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import lds
from db import get_engine
from .config import Settings
from .profiler import Profiler
import trends_writer.trend # noqa
from .trend import TrendManager

TREND_CLASSES = {
    'QUICK': 'TrendQuick',
    'MEAN': 'TrendMean',
    'DERIV': 'TrendDeriv',
    'DIFF': 'TrendDiff'
}


class PipePlant:
    def __init__(self):
        self.queues = {}
        self.read_trends()
        atexit.register(self.shutdown_processes)

    def read_trends(self):
        stmt = (select(lds.Trend, lds.TrendDef)
                .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID)) # noqa
        with Session(get_engine()) as session:
            result = session.execute(stmt).all()

        for trend, trend_def in result:
            try:
                trend_class = getattr(sys.modules["trends_writer.trend"], TREND_CLASSES[trend_def.ID.strip()])
                new_trend = trend_class(trend.ID, Queue(), Settings.db_uri, Profiler.queue)
                TrendManager.add(new_trend)
                if trend_def.ID.strip() == 'QUICK':
                    self.queues[new_trend.register] = new_trend.queue
            except Exception as e:
                logging.warning(f"Trend with id = ({trend.ID}) init error: {e}", exc_info=True)

        for trend in TrendManager.get_all():
            trend.run_trend_process()

    def update(self, register, data):
        try:
            if Settings.use_profiler:
                timestamp = round(time.time())
                Profiler.queue.put((1, timestamp))
                self.queues[register].put((data, timestamp))
            else:
                self.queues[register].put((data, round(time.time())))
        except:
            raise ValueError(f'No quick trend is using {register} register')

    @staticmethod
    def shutdown_processes():
        for trend in TrendManager.get_all():
           trend.queue.put(None)
           trend.process.join()
