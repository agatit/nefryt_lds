import numpy as np
from scipy import signal
from .filter import TrendFilter


class TrendMean(TrendFilter):
    def calculate(self) -> np.ndarray | None:
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            kernel = [1] * (2 * self.window_size * self.block_size + 1)
            norm = 1 / len(kernel)

            result = signal.convolve(self.storage, kernel, mode='valid') * norm

            result = np.maximum(result, [np.iinfo(np.int16).min] * len(result))
            result = np.minimum(result, [np.iinfo(np.int16).max-1] * len(result))  # FFFF reserved for error
            result = result.astype(np.uint16)

            return result
        return None
