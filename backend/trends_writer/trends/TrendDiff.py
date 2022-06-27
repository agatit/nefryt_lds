import logging

import numpy as np

from database import lds
from .TrendCalc import TrendCalc


class TrendDiff(TrendCalc):

    def __init__(self, id: int, parent_id: int = None):
        super().__init__(id, parent_id)
        self.trendID_A = int(self.params['TREND_A'])
        self.trendID_B = int(self.params['TREND_B'])

        self.dict_parentID_data = {
            self.trendID_A: np.array([]),
            self.trendID_B: np.array([])
        }


    def calculate(self, data, parent_id: int = None):

        self.dict_parentID_data[parent_id] = np.append(
            self.dict_parentID_data[parent_id], data)

        # TODO: sprawdzenie czy to drugi update w tej samej chwili
        try:
            diff = self.difference(self.trendID_A, self.trendID_A)
            logging.info(self.__class__.__name__ + ": data calculated")

            return diff, 0

        except Exception as e:
            print(TrendDiff.__name__ + ": " + str(e))
            raise e


    def difference(self, A, B):
        if self.dict_parentID_data[A].size == self.output_size and self.dict_parentID_data[B].size == self.output_size:
            data_A = self.dict_parentID_data[A][:self.output_size]
            data_B = self.dict_parentID_data[B][:self.output_size]

            float_diff = data_A - data_B
            int_diff = float_diff.astype(int)
            self.dict_parentID_data[A] = self.dict_parentID_data[A][self.output_size:]
            self.dict_parentID_data[B] = self.dict_parentID_data[B][self.output_size:]

            return int_diff
        else:
            return None
