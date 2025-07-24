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
from .trend import TrendManager, TrendBase

TREND_CLASSES = {
    'QUICK': 'TrendQuick',
    'MEAN': 'TrendMean',
    'DERIV': 'TrendDeriv',
    'DIFF': 'TrendDiff'
}


logger = logging.getLogger(__name__)


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

        logger.info("PipePlant: Started reading trends")
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
                logger.warning(f"PipePlant: Trend with id = ({trend.ID}) init error: {e}", exc_info=True)

        logger.info(f"PipePlant: Initialized trends (count={len(trend_ids)})")
        Profiler.set_trends(trend_ids, self.double_trends_ids)

        for trend in TrendManager.get_all():
            trend.read_children()
        for register, quick_trend in self.quick_trends.items():
            self.read_trend_children(register, TrendManager.get(quick_trend[0]))
        self.quick_trends_ids_not_updated = list(self.quick_trends_by_ids.keys())
        Profiler.add_profiler_data_to_db(trend_ids)
        for trend in TrendManager.get_all():
            trend.run_trend_process()
        logger.info("PipePlant: Finished reading trends")

    def read_trend_children(self, register: int | None, trend: TrendBase):
        children = trend.children
        if len(children) == 0 and register is None:
            return [trend.id]

        recursive_children = []
        for child in children:
            recursive_children += self.read_trend_children(None, child)

        if register is not None:
            trend.set_children_count(len(recursive_children))
            self.quick_trends_by_ids[trend.id] = recursive_children
            return None
        else:
            trend.set_children_count(len(recursive_children))
            return recursive_children + [trend.id]

    def update(self, register, data):
        try:
            timestamp = round(time.time())
            if timestamp != self.last_timestamp:
                not_updated_count = len(self._prepare_not_updated_trends())
                if not_updated_count != 0:
                    Profiler.queue.put((2, not_updated_count, self.last_timestamp, None, None))
                self.last_timestamp = timestamp
                self.quick_trends_ids_not_updated = list(self.quick_trends_by_ids.keys())
            if self.quick_trends[register][0] in self.quick_trends_ids_not_updated:
                self.quick_trends[register][1].put((data, timestamp, 0))
                self.quick_trends_ids_not_updated.remove(self.quick_trends[register][0])
                logger.debug(f"PipePlant: Trend with id={self.quick_trends[register][0]} data sent (timestamp={timestamp})")
            else:
                logger.warning(f"PipePlant: Quick trend with id = {self.quick_trends[register][0]} already updated (timestamp={timestamp})")
        except KeyError:
            logger.exception(f"PipePlant: No quick trend using register={register}")

    def _prepare_not_updated_trends(self):
        ids = []
        for trend_id in self.quick_trends_ids_not_updated:
            ids += self.quick_trends_by_ids[trend_id]
            ids += [trend_id]

        return ids

    @staticmethod
    def shutdown_processes():
        Profiler.queue.put((-1, None, None))
        for trend in TrendManager.get_all():
            trend.queue.put(None)
            trend.process.terminate()
            trend.process.join(1)
