from typing import List

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

        self._wave_speed = float(self._params['BASE_WAVE_SPEED'])

        # podział na segmenty (jeśli zaimplementujemy więcej niż dwa trendy na metodę)
        self.create_segments()
        

    def create_segments(self) -> None:
        self._segments = []
        previous_trend = None
        for current_trend in self._pressure_deriv_trends:
            if (previous_trend is not None):
                self._segments.append(Segment(self._pipeline.plant, previous_trend, current_trend))
            previous_trend = current_trend
    

    def calc_wave_speed(self) -> int:
        return self._wave_speed

    

    def get_probability(self, begin, end) -> List[List[float]]:
        wave_speed = self.calc_wave_speed()
        
        data_start = data_end = None
        
        self._probability = []
        
        for segment in self._segments:

            # W trakcie pobrania danych musi być jakieś okienko, ze względu na opóźnienie fali
            # Można wymyśleć jakiś zgrabny sposób na jedno zapytanie do bazy danych

            window_begin = begin - segment.window_size(wave_speed)
            window_end = end + segment.window_size(wave_speed)

            data_start = segment.start.get_trend_data(window_begin, window_end)
            data_end = segment.end.get_trend_data(window_begin, window_end)

            for current_time in range(begin, end, self._pipeline.time_resolution):
                probability_row = []

                for current_pos in range(0, segment.length, self._pipeline.length_resolution):
                    l1 = current_pos
                    l2 = segment.length - l1
                    offset1 = int(l1/wave_speed * 100)
                    offset2 = int(l2/wave_speed * 100)
                    data_point = current_time - window_begin
                    data_point = data_point // 10
                    dp1 = min(0, data_start[data_point - offset1])
                    dp2 = min(0, data_end[data_point - offset2])
                    dp3 = min(0, data_start[data_point + offset1])
                    dp4 = min(0, data_end[data_point + offset2])
                    res = dp1 + dp2 - dp3 - dp4
                    res = max(0, (res - self._min_level) / (self._max_level - self._min_level))
                    probability_row.append(res)

                self._probability.append(probability_row)
        
        return self._probability


    def find_leaks_in_range(self, begin, end) -> List[Event]:
        pass


    def find_leaks_to(self, end) -> List[Event]:
        pass       