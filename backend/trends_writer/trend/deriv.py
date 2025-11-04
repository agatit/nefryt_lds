import numpy as np
from scipy import signal
from .filter import TrendFilter


class TrendDeriv(TrendFilter):
    def calculate(self) -> np.ndarray | None:
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            size = int(self.window_size * self.block_size)
            kernel = np.arange(-size, size + 1)
            dt = 1 / self.block_size
            factor = dt * (4 * size + 2) / 3
            norm = 1 / (factor * size * (size + 1) / 2)
            result: np.ndarray = signal.convolve(self.storage, kernel, mode='valid') * -norm

            result = np.clip(result, np.iinfo(np.int16).min, np.iinfo(np.int16).max-1)
            result = result.astype(np.int16)
            return np.flip(result)
        return None
