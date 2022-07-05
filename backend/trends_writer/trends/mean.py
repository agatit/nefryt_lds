from typing import List
import logging
import numpy as np
from scipy import signal

from database import lds
from . import TrendFilter


class TrendMean(TrendFilter):

    def calculate(self) -> np.ndarray:      

        # if len(self.result) == self.output_size then
        # kernel size must be (2 * self.output_size * 100) + 1 and
        # input size must be (2 * self.window_size + 1) * self.output_size
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:

            kernel = [1] * (2 * self.window_size * self.block_size + 1)
            norm = 1/(100*(2*self.window_size+1))

            result = signal.convolve(np.flip(self.storage), kernel, mode='valid') * norm

            # mean is unsigned
            result = np.maximum(result, [np.iinfo(np.uint16).min] * len(result))
            result = np.minimum(result, [np.iinfo(np.uint16).max-1] * len(result))  # FFFF reserved for error
            result = result.astype(np.uint16)

            return result

