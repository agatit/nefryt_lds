from typing import List
import logging
import numpy as np

from ..db import Session
from . import TrendBase


class TrendDiff(TrendBase):

    def __init__(self, id: int, parent_id: int = None):
        super().__init__(id, parent_id)

        self.parent_data = {
            int(self.params['TREND_A']): {
                "data" : np.array([]),
                "timestamp": 0
            },
            int(self.params['TREND_B']): {
                "data" : np.array([]),
                "timestamp": 0
            }
        }


    def update(self, data: List[int], timestamp: int, session: Session, parent_id: int = None):
        logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) updating...")

        with self.lock:
            calculated_data = self.calculate(data, timestamp, parent_id)
            
        if calculated_data is not None:
            super().update(calculated_data, timestamp, session, parent_id)
        else:
            logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) empty calculate result")


    def calculate(self, data: List[int], timestamp: int, parent_id: int = None) -> np.ndarray:

        logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) checking pair...")

        result = None

        if parent_id in self.parent_data.keys():
            self.parent_data[parent_id]["data"] = np.array(data)
            self.parent_data[parent_id]["timestamp"] = timestamp
            
            if list(self.parent_data.values())[0]["timestamp"] == list(self.parent_data.values())[1]["timestamp"]:
                logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) calculating...")
                result = list(self.parent_data.values())[0]["data"] - list(self.parent_data.values())[1]["data"]

                result = np.maximum(result, [np.iinfo(np.int16).min+1] * len(result)) # FFFF reserved for error
                result = np.minimum(result, [np.iinfo(np.int16).max] * len(result))
                result = result.astype(np.int16)

        return result
