import logging
import struct
import time
from multiprocessing import Process
from typing import List
import numpy as np
from sqlalchemy import select, and_, literal, text
from sqlalchemy.orm import Session
from config import setup_engine
from database import lds
from db import get_engine
from multiprocessing.queues import Queue
from trends_writer.trend.trend_manager import TrendManager

logger = logging.getLogger(__name__)


class TrendBase:
    def __init__(self, _id: int, queue: Queue, db_uri: str, profiler_queue: Queue):
        self.id = _id
        self.children: List[TrendBase] = []
        self.params = {}
        self.block_size = 100
        self.profiler_queue = profiler_queue
        self.db_uri = db_uri
        self.queue = queue
        self.children_count = 0
        self._read_params()
        self.process = None
        self.last_update = None

        logger.info(f"{self.__class__.__name__} ({self.id}): Trend initialized (params={self.params})")

    def run_trend_process(self):
        self.process = Process(target=self.process_queue, args=(self.db_uri,))
        self.process.start()
        logger.info(f"{self.__class__.__name__} ({self.id}): Process started")

    def process_queue(self, db_uri: str):
        setup_engine(db_uri)
        self.profiler_queue.put((3, None, int(time.time()), None, None))

        while True:
            item = self.queue.get()
            if item is None:
                for child in self.children:
                    child.queue.put(None)
                break
            data = np.array(item[0])
            logger.debug(f"{self.__class__.__name__} ({self.id}): Got data: {data}")
            timestamp = item[1]
            profiler_timestamp_diff = item[2]
            parent_id = item[3] if len(item) > 3 else None

            if self.last_update is not None and self.last_update < timestamp - 1:
                try:
                    qsize = self.queue.qsize()
                    logger.warning(f"{self.__class__.__name__} ({self.id}): Data not continuously updated "
                                   f"(updated={timestamp - self.last_update} seconds ago, queue size={qsize})")
                except NotImplementedError:
                    logger.warning(f"{self.__class__.__name__} ({self.id}): Data not continuously updated "
                                   f"(updated={timestamp - self.last_update} seconds ago)")

            self.last_update = timestamp
            self.profiler_queue.put((1, self.id, timestamp + profiler_timestamp_diff, time.perf_counter(), None))
            self.update(data, timestamp, profiler_timestamp_diff, parent_id)
            try:
                qsize = self.queue.qsize()
            except NotImplementedError:
                qsize = None
            self.profiler_queue.put((0, self.id, timestamp + profiler_timestamp_diff, time.perf_counter(), qsize))

    def update(self, data: np.ndarray, timestamp: int, profiler_timestamp_diff: int = 0, parent_id: int | None = None):
        self._save(data, timestamp)
        logger.debug(f"{self.__class__.__name__} ({self.id}): Started updating children (timestamp={timestamp})")

        for child in self.children:
            try:
                child.queue.put((data, timestamp, profiler_timestamp_diff, self.id))
            except Exception as e:
                logger.exception(f"{self.__class__.__name__} ({self.id}): "
                                 f"Child {child.__class__.__name__} ({child.id}) update error (timestamp={timestamp}): {e}",
                                 exc_info=True)

        logger.debug(f"{self.__class__.__name__} ({self.id}): Finished updating children (timestamp={timestamp})")
        return timestamp

    def _read_params(self):
        stmt = (select(lds.TrendParamDef, lds.TrendParam)
                .select_from(lds.Trend)
                .join(lds.TrendDef, lds.Trend.TrendDefID == lds.TrendDef.ID)  # noqa
                .join(lds.TrendParamDef, lds.TrendDef.ID == lds.TrendParamDef.TrendDefID)
                .join(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID,
                                           lds.Trend.ID == lds.TrendParam.TrendID))
                .where(lds.Trend.ID == literal(self.id)))

        with Session(get_engine()) as session:
            read_params = session.execute(stmt).fetchall()
        self.params = {}
        for tpd, tp in read_params:
            self.params[tpd.ID.strip()] = tp.Value

    def read_children(self):
        stmt = (select(lds.Trend.ID)
                .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID)  # noqa
                .join(lds.TrendParam, lds.TrendParam.TrendID == lds.Trend.ID)
                .join(lds.TrendParamDef,
                      and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID,
                           lds.TrendDef.ID == lds.TrendParamDef.TrendDefID))
                .where(and_(lds.TrendParamDef.DataType == 'TREND', lds.TrendParam.Value == float(self.id))))

        with Session(get_engine()) as session:
            results = session.execute(stmt).all()

        results = [res[0] for res in results]
        for trend_id in results:
            child_trend = TrendManager.get(trend_id)
            if child_trend is None:
                logger.warning(
                    f"{self.__class__.__name__} ({self.id}): No registered trend with id={trend_id} found for parent")
            else:
                self.children.append(child_trend)
                logger.info(
                    f"{self.__class__.__name__} ({self.id}): Found registered {child_trend.__class__.__name__} ({trend_id})")

    def _save(self, data: np.ndarray, timestamp: int):
        try:
            data = data.astype(np.uint16)
            data = np.minimum(data, [np.iinfo(np.uint16).max - 1] * len(data))  # FFFF reserved for error
            packed_data = struct.pack('<100H', *data)

            insert_stmt = text(f"EXEC Update_Insert_TrendData {self.id}, {timestamp}, :data")
            with Session(get_engine()) as session:
                session.execute(insert_stmt, {"data": packed_data})
                session.commit()

            logger.debug(f"{self.__class__.__name__} ({self.id}): Saved data (timestamp={timestamp})")
        except Exception as e:
            with Session(get_engine()) as session:
                session.rollback()
            logger.exception(f"{self.__class__.__name__} ({self.id}): Update error (timestamp={timestamp}): {e}",
                             exc_info=True)

    def set_children_count(self, children_count: int):
        self.children_count = children_count
