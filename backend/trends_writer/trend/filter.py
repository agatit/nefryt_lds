import struct
from multiprocessing.queues import Queue
from typing import List
import numpy as np
import logging
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from database import lds
from . import TrendBase
from db import get_engine


logger = logging.getLogger(__name__)


class TrendFilter(TrendBase):
    def __init__(self, _id: int, queue: Queue, db_uri: str, profiler_queue: Queue):
        super().__init__(_id, queue, db_uri, profiler_queue)
        self.window_size = int(float(self.params['FILTER_WINDOW']))
        self.storage_timestamp = 0
        self.storage = np.array([], dtype=np.uint16)

    def update(self, data: List[int], timestamp: int, profiler_timestamp_diff: int = 0, parent_id: int = None):
        if timestamp > self.storage_timestamp + 1:
            logger.warning(f"{self.__class__.__name__} ({self.id}): "
                            f"Data in storage not valid (timestamp={timestamp}, storage timestamp={self.storage_timestamp})")
            self.initiate_buffer(self.window_size, timestamp, parent_id)

        if timestamp == self.storage_timestamp + 1 and len(self.storage) < self.block_size * (self.window_size * 2 + 1):
            self.storage = np.append(self.storage[:], data)
        elif timestamp == self.storage_timestamp + 1:
            self.storage = np.append(self.storage[100:], data)
        else:
            logger.warning(f"{self.__class__.__name__} ({self.id}): "
                            f"Data in storage already exists (timestamp={timestamp}, storage timestamp={self.storage_timestamp})")
            self.storage = np.append(self.storage[100:], data)

        self.storage_timestamp = timestamp

        calculated_data = self.calculate()
        if calculated_data is not None:
            super().update(calculated_data, timestamp - self.window_size, profiler_timestamp_diff + self.window_size, parent_id)
            logger.debug(f"{self.__class__.__name__} ({self.id}): Calculated results (timestamp={timestamp})")
        else:
            if self.children_count > 0:
                self.profiler_queue.put((2, self.children_count, timestamp, None, None))
            logger.debug(f"{self.__class__.__name__} ({self.id}): Empty calculation results (timestamp={timestamp})")

        if self.last_update is None:
            self._update_trend_time_delta(profiler_timestamp_diff + self.window_size)

    def calculate(self) -> np.ndarray:
        raise NotImplementedError

    def initiate_buffer(self, window_size: int, timestamp: int, parent_id: int = None):
        logger.debug(f"{self.__class__.__name__} ({self.id}): Started buffer init")
        self.storage = np.array([], dtype=np.uint16)

        stmt = select(lds.TrendData) \
            .where(and_(lds.TrendData.TrendID == parent_id,
            lds.TrendData.Time > timestamp - window_size * 2 - 1,
            lds.TrendData.Time <= timestamp)
        ).order_by(lds.TrendData.Time.desc())  # noqa

        with Session(get_engine()) as session:
            trend_data_iter = session.execute(stmt)
            trend_data = next(trend_data_iter, None)

            last_valid = 0
            for curr_timestamp in range(timestamp - window_size * 2 - 1, timestamp):
                if trend_data is not None and trend_data[0].Time == curr_timestamp:
                    curr_data = struct.unpack('<100h', trend_data[0].Data)
                    curr_data = np.array(curr_data)

                    for i in range(len(curr_data)):
                        if curr_data[i] != 0xFFFF:
                            last_valid = curr_data[i]
                        else:
                            curr_data[i] = last_valid
                    logger.debug(f"{self.__class__.__name__} ({self.id}): Buffer init read data (timestamp={curr_data})")
                elif len(self.storage) > 0:
                    curr_data = np.full(100, fill_value=last_valid, dtype=np.uint16)
                    trend_data = next(trend_data_iter, None)
                    logger.debug(f"{self.__class__.__name__} ({self.id}): Buffer init filled data (timestamp={curr_data})")
                else:
                    curr_data = np.array([])
                    logger.debug(f"{self.__class__.__name__} ({self.id}): Buffer init no data (timestamp={curr_data})")
                self.storage = np.append(curr_data, self.storage)

        self.storage_timestamp = timestamp - 1
        logger.info(f"{self.__class__.__name__} ({self.id}): Buffer init read {len(self.storage)} values from parent trend")
