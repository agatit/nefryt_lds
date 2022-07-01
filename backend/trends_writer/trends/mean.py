from typing import List
import logging
import numpy as np
from scipy import signal

from database import lds
from .filter import TrendFilter


class TrendMean(TrendFilter):

    def calculate(self):      

        # if len(self.result) == self.output_size then
        # kernel size must be (2 * self.output_size * 100) + 1 and
        # input size must be (2 * self.window_size + 1) * self.output_size
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            left = int(-self.window_size * self.block_size)
            right = int(self.window_size * self.block_size) + 1

            kernel = [1] * (2 * self.window_size * self.block_size + 1)
            norm = 1/(self.window_size*(self.window_size+1)/2)

            result = signal.convolve(self.storage, kernel, mode='valid') * norm

            # mean is unsigned
            result = np.maximum(result, [np.iinfo(np.uint16).min] * len(result))
            result = np.minimum(result, [np.iinfo(np.uint16).max] * len(result))
            result = result.astype(np.int16)

            return result            

