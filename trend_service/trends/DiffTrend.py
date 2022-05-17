import logging

import numpy as np

from ..database import orm
from .CalcTrend import CalcTrend


class DiffTrend(CalcTrend):

    def __init__(self, trend: orm.Trend, parent_id):
        super().__init__(trend)
        self.trendID_A = int(self.params['TrendID A'])
        self.trendID_B = int(self.params['TrendID B'])
        self.dict_parentID_data = {self.trendID_A: np.array(
            []), self.trendID_B: np.array([])}
        logging.info(self.__class__.__name__ + ": initialized")

    def calculate(self, data, parent_id: int = None):

        self.dict_parentID_data[parent_id] = np.append(
            self.dict_parentID_data[parent_id], data)

        try:
            diff = self.difference(self.trendID_A, self.trendID_A)
            logging.info(self.__class__.__name__ + ": data calculated")
            return diff
        except Exception as e:
            raise e

    def difference(self, A, B):
        if self.dict_parentID_data[A].size == 100 and self.dict_parentID_data[B].size == 100:
            data_A = self.dict_parentID_data[A][:100]
            data_B = self.dict_parentID_data[B][:100]

            float_diff = data_A - data_B
            int_diff = float_diff.astype(int)
            self.dict_parentID_data[A] = self.dict_parentID_data[A][100:]
            self.dict_parentID_data[B] = self.dict_parentID_data[B][100:]

            return int_diff
        else:
            return None
