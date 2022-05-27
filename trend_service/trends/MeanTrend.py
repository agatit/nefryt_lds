import logging

import numpy as np
from scipy import signal

from ..database import orm
from .CalcTrend import CalcTrend


class MeanTrend(CalcTrend):

    def __init__(self, trend: orm.Trend, parent_id: int = None):
        super().__init__(trend)
        self.window_size = int(self.params['FilterWindow'])
        # print(self.window_size)

        self.max_values_int16 = np.full(
            self.output_size, fill_value=np.iinfo(np.int16).max)
        self.min_values_int16 = np.full(
            self.output_size, fill_value=np.iinfo(np.int16).min)

        self.storage = np.array([])

        self.initalizate_storage_with_recent_trend_data(parent_id)

        logging.info(self.__class__.__name__ + ": initialized")

    def calculate(self, data, parent_id: int = None):

        try:
            # if len(self.result) == self.output_size then
            # kernel size must be (2 * self.output_size * 100) + 1 and
            # input size must be (2 * self.window_size + 1) * self.output_size

            # zgarnac czas z modbusa, dorzucic do calulcate, i zapisac z tym czasem do bazy

            if len(self.storage) >= (2 * self.window_size + 1) * self.output_size:
                kernel = (2 * self.window_size * self.output_size + 1) * \
                    [1/self.window_size]
                # norm = 1/(self.window_size*(self.window_size+1))
                result = list(map(int, signal.convolve(
                    self.storage, kernel, mode='valid')))
                self.storage = self.storage[self.window_size:]

                max_cut = np.maximum(result, self.min_values_int16)
                min_cut = np.minimum(max_cut, self.max_values_int16)

                trunced = min_cut

                logging.info(self.__class__.__name__ + ": data calculated")
                return (trunced, 2 * self.window_size * self.output_size + 1)
            else:
                self.storage = np.append(self.storage, data)
        except Exception as e:
            raise e
