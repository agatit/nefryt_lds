import logging
import struct
from multiprocessing import Process
from typing import List
import numpy as np
from sqlalchemy import select, insert, and_, literal
from sqlalchemy.orm import Session
from database import lds
from db import get_engine
from trends_writer.config import setup_engine
from multiprocessing.queues import Queue
from trends_writer.trend.trend_manager import TrendManager


class TrendBase:
    def __init__(self, _id: int, queue: Queue, db_uri: str, profiler_queue: Queue | None):
        self.id = _id
        self.children: List[TrendBase] = []
        self.params = {}
        self.block_size = 100
        self.profiler_queue = profiler_queue
        self.db_uri = db_uri
        self.queue = queue

        self._read_params()
        self.process = None

        logging.info(f"{self.__class__.__name__} ({self.id}) initialized: params={self.params}")

    def run_trend_process(self):
        self._read_children()
        self.process = Process(target=self.process_queue, args=(self.db_uri, ))
        self.start_process_queue()
        logging.info(f"{self.__class__.__name__} ({self.id}) started")

    def start_process_queue(self):
        self.process.start()

    def process_queue(self, db_uri: str):
        setup_engine(db_uri)

        while True:
            item = self.queue.get()
            if item is None:
                for child in self.children:
                    child.queue.put(None)
                    child.process.join()
                break
            data = np.array(item[0])
            timestamp = item[1]
            parent_id = item[2] if len(item) > 2 else None

            self.update(data, timestamp, parent_id)
            if self.profiler_queue:
                self.profiler_queue.put((0, timestamp))

    def update(self, data: np.ndarray, timestamp: int, parent_id: int | None = None):
        self._save(data, timestamp)
        logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) updating children...")

        for child in self.children:
            try:
                if self.profiler_queue:
                    self.profiler_queue.put((1, timestamp))
                child.queue.put((data, timestamp, self.id))
            except Exception as e:
                logging.exception(f"{timestamp} {self.__class__.__name__} ({self.id}) child {child.__class__.__name__} ({child.id}) update error: {e}", exc_info=True)

        return timestamp

    def _read_params(self):
        stmt = (select(lds.TrendParamDef, lds.TrendParam)
                .select_from(lds.Trend)
                .join(lds.TrendDef, lds.Trend.TrendDefID == lds.TrendDef.ID) # noqa
                .join(lds.TrendParamDef, lds.TrendDef.ID == lds.TrendParamDef.TrendDefID)
                .join(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID, lds.Trend.ID == lds.TrendParam.TrendID))
                .where(lds.Trend.ID == literal(self.id)))

        with Session(get_engine()) as session:
            read_params = session.execute(stmt).fetchall()
        self.params = {}
        for tpd, tp in read_params:
            self.params[tpd.ID.strip()] = tp.Value

    def _read_children(self):
        stmt = (select(lds.Trend.ID)
                .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID) # noqa
                .join(lds.TrendParam, lds.TrendParam.TrendID == lds.Trend.ID)
                .join(lds.TrendParamDef,
                      and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID,
                           lds.TrendDef.ID == lds.TrendParamDef.TrendDefID))
                .where(and_(lds.TrendParamDef.DataType == 'TREND', lds.TrendParam.Value == float(self.id))))

        with Session(get_engine()) as session:
            results = session.execute(stmt).all()

        for trend_id in results:
            trend_id = trend_id[0]
            child_trend = TrendManager.get(trend_id)
            if child_trend is None:
                logging.warning(f"No registered Trend ({trend_id}) found for parent {self.__class__.__name__} ({self.id})")
            else:
                self.children.append(child_trend)
                logging.info(f"Found registered {child_trend.__class__.__name__} ({trend_id}) for parent {self.__class__.__name__} ({self.id})")

    def _save(self, data: np.ndarray, timestamp: int):
        try:
            data = data.astype(np.uint16)
            data = np.minimum(data, [np.iinfo(np.uint16).max-1] * len(data))  # FFFF reserved for error
            packed_data = struct.pack('<100H', *data)

            insert_stmt = insert(lds.TrendData).values(
                TrendID=self.id,
                Time=timestamp,
                Data=packed_data
            )
            with Session(get_engine()) as session:
                session.execute(insert_stmt)
                session.commit()

            logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) saved") 
        except Exception as e:
            with Session(get_engine()) as session:
                session.rollback()
            raise e
