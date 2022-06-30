from typing import List
import logging
import numpy as np

from database import lds
from .filter import TrendBase


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


    def update(self, data: List[int], timestamp: int, parent_id: int = None):
        logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) updating...")

        calculated_data = self.calculate(data, timestamp, parent_id)
        if calculated_data is not None:
            super().update(calculated_data, timestamp, parent_id)
        else:
            logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) empty calculate result")


    def calculate(self, data: List[int], timestamp: int, parent_id: int = None):

        logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) checking pair...")

        diff = None

        if parent_id in self.parent_data.keys():
            self.parent_data[parent_id]["data"] = np.array(data)
            self.parent_data[parent_id]["timestamp"] = timestamp
            
            if list(self.parent_data.values())[0]["timestamp"] == list(self.parent_data.values())[1]["timestamp"]:
                logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) calculating...")
                diff = list(self.parent_data.values())[0]["data"] - list(self.parent_data.values())[1]["data"]

        return diff
