import atexit
import logging
import time
from multiprocessing import Queue
from sqlalchemy import select
from sqlalchemy.orm import Session
from config import Settings
from database import lds
from db import get_engine
import trends_writer.trend # noqa
from .trends import TrendBase, TrendMean, TrendDeriv, TrendDiff
from .trend_manager import TrendManager

TREND_CLASSES = {
    'QUICK': TrendBase,
    'MEAN': TrendMean,
    'DERIV': TrendDeriv,
    'DIFF': TrendDiff
}

logger = logging.getLogger(__name__)


class PipePlant:
    def __init__(self, quick_trend_ids: list):
        self.plant_queue = Queue()
        self.quick_trends = {}
        self.read_trends(quick_trend_ids)
        self.last_timestamp = round(time.time())
        atexit.register(self.shutdown_processes)

    def read_trends(self, quick_trend_ids: list):
        stmt = (select(lds.Trend, lds.TrendDef)
                .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID)) # noqa
        logger.info("PipePlant: Started reading trends")
        with Session(get_engine()) as session:
            result = session.execute(stmt).all()

        trend_ids = []
        for trend, trend_def in result:
            try:
                trend_def_id = trend_def.ID.strip()
                if trend_def_id == 'QUICK' and trend.ID in quick_trend_ids or trend_def_id != 'QUICK':
                    trend_class = TREND_CLASSES[trend_def_id]
                    new_trend = trend_class(trend.ID, Queue(), Settings.db_uri)
                    trend_ids.append(trend.ID)
                    TrendManager.add(new_trend)
                    if trend_def_id == 'QUICK':
                        self.quick_trends[trend.ID] = (new_trend, new_trend.queue)
            except Exception as e:
                logger.warning(f"PipePlant: Trend with id = ({trend.ID}) init error: {e}", exc_info=True)

        logger.info(f"PipePlant: Initialized trends (count={len(trend_ids)})")

        for trend in TrendManager.get_all():
            trend.read_children()

        for trend, _ in self.quick_trends.values():
            self.read_trend_expected_calls(trend)

        for trend in TrendManager.get_all():
            trend.run_trend_process(self.plant_queue)

        time.sleep(5)
        logger.info("PipePlant: Finished reading trends")

    def read_trend_expected_calls(self, trend: TrendBase):
        children = trend.children
        if len(children) == 0:
            return trend.expected_calls

        recursive_calls = trend.expected_calls
        for child in children:
            recursive_calls += self.read_trend_expected_calls(child)

        trend.expected_calls = recursive_calls
        return trend.expected_calls

    def update(self, quick_trend_data: dict, timestamp: int):
        expected_responses = 0
        for trend_id, data in quick_trend_data.items():
            self.quick_trends[trend_id][1].put((data, timestamp))
            expected_responses += self.quick_trends[trend_id][0].expected_calls
            logger.debug(f"PipePlant: Trend with id={trend_id} data sent (timestamp={timestamp})")
        responses = 0
        while responses < expected_responses:
            self.plant_queue.get()
            responses += 1

    @staticmethod
    def shutdown_processes():
        for trend in TrendManager.get_all():
            trend.queue.put(None)
            trend.process.terminate()
            trend.process.join(1)
