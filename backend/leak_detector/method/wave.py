import logging
from os import times_result
from typing import List

import numpy

from .base import MethodBase, Segment
from ..plant import Event


class MethodWave(MethodBase):

    def __init__(self, pipeline, id, name):
        super().__init__(pipeline, id, name)
        # skopiowanie specyficznych parametrów metody:
        # TODO: rozważyć obsługe błedów przy czytaniu parmatrów, np. przypisanie nieistnijącego trendu

        self._pressure_deriv_trends = []
        for trend_id in self._params['PRESSURE_DERIV_TRENDS'].split(','):
            self._pressure_deriv_trends.append(pipeline.plant.trends[int(trend_id)])
        # etc.

        self._max_level = float(self._params['MAX_LEVEL'])
        self._min_level = float(self._params['MIN_LEVEL'])
        self._alarm_level = float(self._params['ALARM_LEVEL'])

        # podział na segmenty (jeśli zaimplementujemy więcej niż dwa trendy na metodę)
        self.create_segments()
        

    def create_segments(self) -> None:
        self._segments = []
        previous_trend = None
        for current_trend in self._pressure_deriv_trends:
            if (previous_trend is not None):
                self._segments.append(Segment(self._pipeline.plant, previous_trend, current_trend))
            previous_trend = current_trend
        

    #Dodałem parametr dot. czasu sprawdzanego wycieku
    def get_probability(self, begin, end, step) -> List[float]:
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

        #Powinna być jakaś funkcja która to liczy
        wave_speed = 1000 
        
        data_start = data_end = None
        
        probability = []

        for segment in self._segments:

            # W trakcie pobrania danych musi być jakieś okienko, ze względu na opóźnienie fali
            window_begin = begin - 40
            window_end = end + 40

            #Tylko jedne zapytanie na trend do bazy danych
            if data_start is None:    
                data_start = segment.start.get_trend_data(window_begin, window_end)
            
            data_end = segment.end.get_trend_data(window_begin, window_end)
            for current_time in range(begin, end, step): #skok o step czy o time_resolution?
                probability_row = []

                for current_pos in range(0, segment.length, self._pipeline.length_resolution):
                    l1 = current_pos
                    l2 = segment.length - l1
                    offset1 = int(l1/wave_speed * 100)
                    offset2 = int(l2/wave_speed * 100)
                    start = current_time - window_begin
                    dp1 = min(0, data_start[start - offset1])
                    dp2 = min(0, data_end[start - offset2])
                    dp3 = min(0, data_start[start + offset1])
                    dp4 = min(0, data_end[start + offset2])
                    res = dp1 + dp2 - dp3 - dp4
                    res = (res - self._min_level) / (self._max_level - self._min_level)
                    probability_row.append(res)

                probability.append(probability_row)
        
            data_start = data_end

        return probability


    def find_leaks_in_range(self, begin, end) -> List[Event]:
        pass


    def find_leaks_to(self, end) -> List[Event]:
        pass       