import logging
import struct
from multiprocessing import Process
import numpy as np
from scipy import signal
from sqlalchemy import select, and_, literal, text
from sqlalchemy.orm import Session
from config import setup_engine
from database import lds
from db import get_engine
from multiprocessing.queues import Queue
from trend_manager import TrendManager

logger = logging.getLogger(__name__)


class TrendBase:
    def __init__(self, id_: int, queue: Queue, db_uri: str):
        self.id = id_
        self.children: list[TrendBase] = []
        self.params = {}
        self.block_size = 100
        self.db_uri = db_uri
        self.queue = queue
        self._read_params()
        self.expected_calls = 0
        self.process = None

        logger.info(f"{self.__class__.__name__} ({self.id}): Trend initialized (params={self.params})")

    def run_trend_process(self, plant_queue: Queue):
        self.process = Process(target=self.process_queue, args=(self.db_uri, plant_queue))
        self.process.start()
        logger.info(f"{self.__class__.__name__} ({self.id}): Process started")

    def process_queue(self, db_uri: str, plant_queue: Queue):
        setup_engine(db_uri)
        while True:
            item = self.queue.get()
            if item is None:
                for child in self.children:
                    child.queue.put(None)
                break
            data = np.array(item[0])
            logger.debug(f"{self.__class__.__name__} ({self.id}): Got data: {data}")
            timestamp = item[1]
            parent_id = item[2] if len(item) > 2 else None
            self.update(data, timestamp, parent_id)
            if parent_id is not None:
                plant_queue.put(self.id)

    def update(self, data: np.ndarray, timestamp: int, parent_id: int | None = None):
        # if parent_id is not None:
        self._save(data, timestamp)
        logger.debug(f"{self.__class__.__name__} ({self.id}): Started updating children (timestamp={timestamp})")

        for child in self.children:
            try:
                child.queue.put((data, timestamp, self.id))
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

            insert_stmt = text(f"EXEC Update_Insert_PastTrendData {self.id}, {timestamp}, :data")
            with Session(get_engine()) as session:
                session.execute(insert_stmt, {"data": packed_data})
                session.commit()

            logger.debug(f"{self.__class__.__name__} ({self.id}): Saved data (timestamp={timestamp})")
        except Exception as e:
            with Session(get_engine()) as session:
                session.rollback()
            logger.exception(f"{self.__class__.__name__} ({self.id}): Update error (timestamp={timestamp}): {e}",
                             exc_info=True)


class TrendFilter(TrendBase):
    def __init__(self, id_: int, queue: Queue, db_uri: str):
        super().__init__(id_, queue, db_uri)
        self.window_size = int(float(self.params['FILTER_WINDOW']))
        self.storage_timestamp = 0
        self.storage = np.array([], dtype=np.uint16)
        self.expected_calls = 1

    def update(self, data: list[int], timestamp: int, parent_id: int = None):
        data = np.flip(data)
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
            super().update(calculated_data, timestamp - self.window_size, parent_id)
            logger.debug(f"{self.__class__.__name__} ({self.id}): Calculated results (timestamp={timestamp})")
        else:
            logger.debug(f"{self.__class__.__name__} ({self.id}): Empty calculation results (timestamp={timestamp})")

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
                    curr_data = np.flip(curr_data)

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


class TrendDeriv(TrendFilter):
    def calculate(self) -> np.ndarray | None:
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            size = int(self.window_size * self.block_size)
            kernel = np.arange(-size, size + 1)
            dt = 1 / self.block_size
            factor = dt * (4 * size + 2) / 3
            norm = 1 / (factor * size * (size + 1) / 2)
            # TODO: change multiplication to params manipulation
            result: np.ndarray = signal.convolve(self.storage, kernel, mode='valid') * -norm * 10

            result = np.clip(result, np.iinfo(np.int16).min-1, np.iinfo(np.int16).max)
            result = result.astype(np.int16)
            return np.flip(result)
        return None


class TrendMean(TrendFilter):
    def calculate(self) -> np.ndarray | None:
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            kernel = [1] * (2 * self.window_size * self.block_size + 1)
            norm = 1 / len(kernel)

            result = signal.convolve(self.storage, kernel, mode='valid') * norm

            result = np.clip(result, np.iinfo(np.int16).min-1, np.iinfo(np.int16).max)
            result = result.astype(np.uint16)
            return np.flip(result)
        return None


class TrendDiff(TrendBase):
    def __init__(self, id_: int, queue: Queue, db_uri: str):
        super().__init__(id_, queue, db_uri)
        if self.params['TREND_A'] == self.params['TREND_B']:
            raise BaseException('Trend A has to be different then Trend B')

        self.parent_data = {
            int(self.params['TREND_A']): {
                "data": np.array([]),
                "timestamp": 0
            },
            int(self.params['TREND_B']): {
                "data": np.array([]),
                "timestamp": 0
            }
        }
        self.expected_calls = 2

    def update(self, data: list[int], timestamp: int, parent_id: int | None = None):
        calculated_data = self.calculate(data, timestamp, parent_id)

        if calculated_data is not None:
            super().update(calculated_data, timestamp, parent_id)
            logger.debug(f"{self.__class__.__name__} ({self.id}): Calculated results (timestamp={timestamp})")
        else:
            logger.debug(f"{self.__class__.__name__} ({self.id}): Empty calculation results (timestamp={timestamp})")

    def calculate(self, data: list[int], timestamp: int, parent_id: int | None = None) -> np.ndarray:
        result = None

        if parent_id in self.parent_data.keys():
            self.parent_data[parent_id]["data"] = np.array(data)
            self.parent_data[parent_id]["timestamp"] = timestamp

            if list(self.parent_data.values())[0]["timestamp"] == list(self.parent_data.values())[1]["timestamp"]:
                result = list(self.parent_data.values())[0]["data"] - list(self.parent_data.values())[1]["data"]

                result = np.clip(result, np.iinfo(np.int16).min-1, np.iinfo(np.int16).max)
                result = result.astype(np.int16)

        return result
