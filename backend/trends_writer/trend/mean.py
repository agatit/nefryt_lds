import numpy as np
from scipy import signal
from .filter import TrendFilter


class TrendMean(TrendFilter):
    def calculate(self) -> np.ndarray | None:
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            kernel = [1] * (2 * self.window_size * self.block_size + 1)
            norm = 1 / len(kernel)

            result = signal.convolve(self.storage, kernel, mode='valid') * norm

            result = np.clip(result, np.iinfo(np.int16).min-1, np.iinfo(np.int16).max)
            result = result.astype(np.uint16)
            return np.flip(result)
        return None
