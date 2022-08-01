import logging
from typing import List

from .base import MethodBase
from ..plant import Event


class MethodWave(MethodBase):

    def __init__(self, pipeline, id, name):
        super().__init__(pipeline, id, name)
        # skopiowanie specyficznych parametrów metody:
        # TODO: rozważyć obsługe błedów przy czytaniu parmatrów, np. przypisanie nieistnijącego trendu
        self._pressure_deriv_trend_1 = pipeline.plant.trends[int(self._params['PRESSURE_DERIV_TREND_1'])]
        self._pressure_deriv_trend_2 = pipeline.plant.trends[int(self._params['PRESSURE_DERIV_TREND_2'])]
        # etc.

        # podział na segmenty (jeśli zaimplementujemy więcej niż dwa trendy na metodę)
        # może zamiast PRESSURE_DERIV_TREND zrobić PRESSURE_DERIV_LIST z ID trendów oddzielonych przecinkami...

        # wyznacznie odległości pomiędzy pomiarami
        # segment[0].length = ...
        

    def get_probablity(self, timestamp) -> List[float]:

        # probability = [[]]
        #dla każdego segmentu:
            #dla każdej rozpatrywanej chwili w czasie (current_time):
                #dle każdego punku w długości (current_pos):
                    # l1 = current_pos - begin_pos
                    # l2 = end_pos - current_pos
                    # dp1 = pressure_deriv_trend_1.get_value(current_time - l1/wave_speed)
                    # dp2 = pressure_deriv_trend_2.get_value(current_time - l2/wave_speed)
                    # dp3 = pressure_deriv_trend_1.get_value(current_time + l1/wave_speed)
                    # dp4 = pressure_deriv_trend_2.get_value(current_time + l2/wave_speed)
                    # dp1 = min(dp1, 0) # wyzrost ciśnienia to na pewno nie wyciek
                    # dp2 = ...itd.             
                    # probability[current_time][current_pos] = normalize(dp1 + dp2 - dp3 - dp4)
                    #
                    # normalizacja na podstawie parametrów min, max i alarm metody 
                    # wave_speed docelowo powinno być funkcją składającą śrendią prędkość na podstawie danych z nodów i linków
        pass


    def find_leaks_in_range(self, begin, end) -> List[Event]:
        pass


    def find_leaks_to(self, end) -> List[Event]:
        pass       