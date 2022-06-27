import logging

import numpy as np
from scipy import signal

from database import lds
from .TrendCalc import TrendCalc


class TrendDeriv(TrendCalc):

    def __init__(self, trend: lds.Trend, parent_id: int = None):
        super().__init__(trend, parent_id)
        self.window_size = int(self.params['FILTER_WINDOW'])

        self.max_values_int16 = np.full(
            self.output_size, fill_value=np.iinfo(np.int16).max)
        self.min_values_int16 = np.full(
            self.output_size, fill_value=np.iinfo(np.int16).min)
    
        self.storage = self.initiate_buffer(parent_id)


    def calculate(self, data, parent_id: int = None):

        # if len(self.result) == self.output_size then
        # kernel size must be (2 * self.output_size * 100) + 1 and
        # input size must be (2 * self.window_size + 1) * self.output_size
        if len(self.storage) >= (2 * self.window_size + 1) * self.output_size:
            left = int(-self.window_size * self.output_size)
            right = int(self.window_size * self.output_size) + 1

            kernel = np.array(
                list(range(left, right)))
            norm = 1/(self.window_size*(self.window_size+1)/2)

            result = list(map(int, signal.convolve(
                self.storage, kernel, mode='valid') * norm))
            self.storage = self.storage[self.output_size:]

            max_cut = np.maximum(result, self.min_values_int16)
            min_cut = np.minimum(max_cut, self.max_values_int16)

            trunced = min_cut
            logging.info(self.__class__.__name__ + ": data calculated")

            return trunced, 2 * self.window_size * self.output_size + 1

        else:
            self.storage = np.append(self.storage, data)

            return None, None # to chyba powinno być exception!
