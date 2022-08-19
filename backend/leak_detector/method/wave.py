from typing import List

import numpy as np

from .base import MethodBase, Segment
from ..plant import Event, Pipeline

import matplotlib.pyplot as plt
class MethodWave(MethodBase):

    def __init__(self, pipeline : Pipeline, id, name):
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

        self._wave_speed = float(self._params['BASE_WAVE_SPEED'])


        self._segments = []
        self._length_pipeline = 0

        self.create_segments()
        

    def create_segments(self) -> None:
        previous_trend = None
        for current_trend in self._pressure_deriv_trends:
            if (previous_trend is not None):
                segment = Segment(self._pipeline, previous_trend, current_trend,
                                     self._length_pipeline, self._wave_speed)
                self._length_pipeline += segment.length
                self._segments.append(segment)
            previous_trend = current_trend
    
    def get_segment(self, position) -> Segment:
        for segment in self._segments:
            if (segment._begin_pos <= position <= segment._end_pos):
                return segment
        return None

    
    def get_probability(self, begin, end) -> List[List[float]]:
        probability = []
        previous_segment = None
        for current_pos in range(0, self._length_pipeline, self._pipeline.length_resolution):
            probability_pos = []
            segment = self.get_segment(current_pos)
            wave_speed = segment.calc_wave_speed(current_pos)

            if (previous_segment != segment):
                window_begin = begin - segment.max_window_size
                window_end = end + segment.max_window_size

                data_start = segment.start.get_trend_data(window_begin, window_end)
                data_end = segment.end.get_trend_data(window_begin, window_end)

            l1 = current_pos - segment._begin_pos
            l2 = segment._end_pos - current_pos

            for current_time in range(begin, end, self._pipeline.time_resolution):
                offset1 = (l1 * 1000) / wave_speed 
                offset2 = (l2 * 1000) / wave_speed 
                data_point = current_time - window_begin
                
                dp1 = data_start[int((data_point - offset1) / 10)]
                dp2 = data_end[int((data_point - offset2) / 10)]
                dp3 = data_start[int((data_point + offset1) / 10)]
                dp4 = data_end[int((data_point + offset2) / 10)]
                
                res = dp1 + dp2 - dp3 - dp4
                
                res = (res - self._min_level) / (self._max_level - self._min_level)

                res = min(max(0, res), 1)
                
                probability_pos.append(res)

            previous_segment = segment
            probability.append(probability_pos)

        return probability


    def find_leaks_in_range(self, begin, end) -> List[Event]:
        probabilities = np.array(self.get_probability(begin, end))
        
        events = []

        for position in range(len(probabilities)):
            for time in range(len(probabilities[0])):
                if (probabilities[position][time] < self._alarm_level):
                    probabilities[position][time] = 0

        # Miejsce na algorytm:

        fig, ax = plt.subplots()
        ax.imshow(probabilities)
        plt.show()

        return events


    def find_leaks_to(self, end) -> List[Event]:
        pass