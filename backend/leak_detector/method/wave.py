import logging
from typing import List

from .base import MethodBase


class MethodWave(MethodBase):

    def __init__(self, pipeline, id, name):
        super().__init__(pipeline, id, name)
        # skopiowanie specyficznych parametrów metody:
        # TODO: rozważyć obsługe błedów przy czytaniu parmatrów, np. przypisanie nieistnijącego trendu
        self._pressure_deriv_trend_1 = pipeline.plant.trends[int(self._params['PRESSURE_DERIV_TREND_1'])]
        self._pressure_deriv_trend_2 = pipeline.plant.trends[int(self._params['PRESSURE_DERIV_TREND_2'])]
        # etc.

        # węzły z pomiarami ciśnienia powinny być rozpoznawane z siatki link/node
        # trzeba wymyslić jak rozpoznać który trend pochodnej jest związny z dana metodą
        # 
        

    def get_probablity(self, timestamp, step) -> List[float]:
        pass    