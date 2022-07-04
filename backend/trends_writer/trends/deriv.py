from typing import List
import logging
import numpy as np
from scipy import signal
import time

from database import lds
from .filter import TrendFilter


class TrendDeriv(TrendFilter):


    def calculate(self) -> np.ndarray:      

        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            size = int(self.window_size * self.block_size)

            kernel = np.array(range(-size, size+1))
            norm = 1/(self.block_size * self.window_size * (self.block_size * self.window_size+1)/2)

            result = signal.convolve(np.flip(self.storage), kernel, mode='valid') * norm

            # drivative is signed
            result = np.maximum(result, [np.iinfo(np.int16).min+1] * len(result)) # FFFF reserved for error
            result = np.minimum(result, [np.iinfo(np.int16).max] * len(result))
            result = result.astype(np.int16)

            return result
