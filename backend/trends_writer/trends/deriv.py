from typing import List
import logging
import numpy as np
from scipy import signal
import time

from database import lds
from .filter import TrendFilter


class TrendDeriv(TrendFilter):


    def calculate(self):      

        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            left = int(-self.window_size * self.block_size)
            right = int(self.window_size * self.block_size) + 1

            kernel = np.array(range(left, right))
            norm = 1/(100*self.window_size*(100*self.window_size+1)/2)

            result = signal.convolve(self.storage, kernel, mode='valid') * norm

            # drivative is signed
            result = np.maximum(result, [np.iinfo(np.int16).min] * len(result))
            result = np.minimum(result, [np.iinfo(np.int16).max] * len(result))
            result = result.astype(np.int16)

            return result
