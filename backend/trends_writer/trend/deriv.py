from multiprocessing import Queue
import numpy as np
from scipy import signal
from .filter import TrendFilter


class TrendDeriv(TrendFilter):
    def __init__(self, id_: int, queue: Queue, db_uri: str, profiler_queue: Queue):
        super().__init__(id_, queue, db_uri, profiler_queue)
        self.expected_to_raw_coef = float(self.params.get('EXPECTED_TO_RAW_COEF', 1))

    def calculate(self) -> np.ndarray | None:
        if len(self.storage) >= (2 * self.window_size + 1) * self.block_size:
            size = int(self.window_size * self.block_size)
            kernel = np.arange(-size, size + 1)
            dt = 1 / self.block_size
            factor = dt * (4 * size + 2) / 3
            norm = self.expected_to_raw_coef / (factor * size * (size + 1) / 2)
            result: np.ndarray = signal.convolve(self.storage, kernel, mode='valid') * -norm

            result = np.clip(result, np.iinfo(np.int16).min-1, np.iinfo(np.int16).max)
            result = result.astype(np.int16)
            return np.flip(result)
        return None
