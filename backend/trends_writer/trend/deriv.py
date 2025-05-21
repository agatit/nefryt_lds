import numpy as np
from scipy import signal
from . import TrendFilter


class TrendDeriv(TrendFilter):
    def calculate(self) -> np.ndarray | None:
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            size = int(self.window_size * self.block_size)

            kernel = np.arange(-size, size + 1)
            dt = 1 / self.block_size
            norm = 1 / (dt * np.sum(kernel ** 2))
            result = signal.convolve(self.storage, kernel, mode='valid') * -norm

            # derivative is signed
            result = np.maximum(result, [np.iinfo(np.int16).min + 1] * len(result))  # FFFF reserved for error
            result = np.minimum(result, [np.iinfo(np.int16).max] * len(result))
            result = result.astype(np.int16)

            return result
        return None
