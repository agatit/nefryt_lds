import logging
from typing import List

from .base import MethodBase


class MethodWave(MethodBase):

    def __init__(self, pipeline, id, name):
        super().__init__(pipeline, id, name)
        # skopiowanie specyficznych parametrów metody:
        self._pressure_trend1 = self._params['PRESSURE_TREND_1']
        self._pressure_trend2 = self._params['PRESSURE_TREND_2']
        # etc.
        

    def get_probablity(self, timestamp, step) -> List[float]:
        pass    