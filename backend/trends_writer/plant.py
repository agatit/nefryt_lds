import atexit
import time
from multiprocessing import Queue
from sqlalchemy import select, literal
from sqlalchemy.orm import Session
from database import lds
from db import get_engine
from .config import Settings
from .profiler import Profiler
from .trend import TrendQuick


class PipePlant:
    def __init__(self):
        self.trends = []
        self.queues = {}
        self.read_trends()
        atexit.register(self.shutdown_processes)

    def read_trends(self):
        stmt = (select(lds.Trend)
                .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID)  # noqa
                .where(lds.TrendDef.ID == literal('QUICK')))
        with Session(get_engine()) as session:
            result = session.execute(stmt).fetchall()

        for trend in result:
            queue = Queue()
            new_trend_quick = TrendQuick(trend[0].ID, queue, Profiler.queue)
            self.trends.append(new_trend_quick)
            self.queues[new_trend_quick.register] = new_trend_quick.queue

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

    def shutdown_processes(self):
        for trend in self.trends:
           trend.queue.put(None)
           trend.process.join()
