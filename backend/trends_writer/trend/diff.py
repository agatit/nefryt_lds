from multiprocessing.queues import Queue
import logging
import numpy as np
from . import TrendBase


logger = logging.getLogger(__name__)


class TrendDiff(TrendBase):
    def __init__(self, id_: int, queue: Queue, db_uri: str, profiler_queue: Queue | None):
        super().__init__(id_, queue, db_uri, profiler_queue)
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

    def update(self, data: list[int], timestamp: int, profiler_timestamp_diff: int = 0, parent_id: int | None = None):
        calculated_data = self.calculate(data, timestamp, parent_id)

        if calculated_data is not None:
            super().update(calculated_data, timestamp, profiler_timestamp_diff, parent_id)
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

                result = np.maximum(result, [np.iinfo(np.int16).min + 1] * len(result))  # FFFF reserved for error
                result = np.minimum(result, [np.iinfo(np.int16).max] * len(result))
                result = result.astype(np.int16)

        return result
