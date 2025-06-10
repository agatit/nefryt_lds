import atexit
import logging
import sys
import time
from collections import Counter
from multiprocessing import Queue
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import lds
from db import get_engine
from .config import Settings
from .profiler import Profiler
import trends_writer.trend # noqa
from .trend import TrendManager, TrendBase

TREND_CLASSES = {
    'QUICK': 'TrendQuick',
    'MEAN': 'TrendMean',
    'DERIV': 'TrendDeriv',
    'DIFF': 'TrendDiff'
}


class PipePlant:
    def __init__(self):
        self.quick_trends = {}
        self.quick_trends_by_ids = {}
        self.quick_trends_ids_not_updated = []
        self.double_trends_ids = []
        self.read_trends()
        self.last_timestamp = round(time.time())
        atexit.register(self.shutdown_processes)

    def read_trends(self):
        stmt = (select(lds.Trend, lds.TrendDef)
                .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID)) # noqa
        with Session(get_engine()) as session:
            result = session.execute(stmt).all()

        trend_ids = []
        for trend, trend_def in result:
            try:
                trend_class = getattr(sys.modules["trends_writer.trend"], TREND_CLASSES[trend_def.ID.strip()])
                new_trend = trend_class(trend.ID, Queue(), Settings.db_uri, Profiler.queue)
                trend_ids.append(trend.ID)
                TrendManager.add(new_trend)
                if trend_def.ID.strip() == 'QUICK':
                    self.quick_trends[new_trend.register] = (trend.ID, new_trend.queue)
                elif trend_def.ID.strip() == 'DIFF':
                    self.double_trends_ids.append(trend.ID)
            except Exception as e:
                logging.warning(f"Trend with id = ({trend.ID}) init error: {e}", exc_info=True)

        Profiler.set_trends(trend_ids, self.double_trends_ids)

        for trend in TrendManager.get_all():
            trend.read_children()
        for register, quick_trend in self.quick_trends.items():
            self.read_trend_children(register, TrendManager.get(quick_trend[0]))
        self.quick_trends_ids_not_updated = list(self.quick_trends_by_ids.keys())
        for trend in TrendManager.get_all():
            trend.run_trend_process()

    def read_trend_children(self, register: int | None, trend: TrendBase):
        children = trend.children
        if len(children) == 0 and register is None:
            return [trend.id]

        recursive_children = []
        for child in children:
            recursive_children += self.read_trend_children(None, child)

        if register is not None:
            self.quick_trends_by_ids[trend.id] = recursive_children
            return None
        else:
            return recursive_children + [trend.id]

    def update(self, register, data):
        try:
            timestamp = round(time.time())
            print(timestamp)
            if timestamp != self.last_timestamp:
                self.last_timestamp = timestamp
                not_updated_count = self._prepare_not_updated_trends()
                Profiler.queue.put((2, not_updated_count, timestamp-1))
                self.quick_trends_ids_not_updated = list(self.quick_trends_by_ids.keys())
            if self.quick_trends[register][0] in self.quick_trends_ids_not_updated:
                self.quick_trends[register][1].put((data, timestamp))
                self.quick_trends_ids_not_updated.remove(self.quick_trends[register][0])
            else:
                raise Exception(f"Quick trend with id = {self.quick_trends[register][0]} already updated in timestamp {timestamp}")
        except KeyError:
            raise ValueError(f'No quick trend is using {register} register')

    def _prepare_not_updated_trends(self):
        ids = []
        for trend_id in self.quick_trends_ids_not_updated:
            ids += self.quick_trends_by_ids[trend_id]
            ids += [trend_id]

        counter = Counter(ids)
        total = 0

        for trend_id, count in counter.items():
            if trend_id in self.double_trends_ids:
                total += count
            else:
                total += 1

        return total

    @staticmethod
    def shutdown_processes():
        for trend in TrendManager.get_all():
           trend.queue.put(None)
           trend.process.join()
