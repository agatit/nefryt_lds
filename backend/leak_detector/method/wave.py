import logging
from math import ceil
from typing import List
import numpy as np
#from ..tests.plots import global_plot

from .base import MethodBase
from ..trend import Trend
from ..plant import Event, Pipeline

# Obecna wersja zakłada, że segmenty mają stały wave speed.
# Może wpakować to jako podklasy Klasy MethodBase?
class Segment:
    def __init__(self, pipeline: Pipeline, start: Trend, end: Trend, begin_pos: int, wave_speed: float) -> None:
        distances = pipeline.plant.get_distances(pipeline.plant.nodes[start.node_id], pipeline.plant.nodes[end.node_id])
        if (len(distances) > 1 or len(distances) == 0):
            logging.exception(f"There isn't exactly one path between {start.id} and {end.id}.")
            raise
        self._length = distances[0]
        self._start = start
        self._end = end
        self._begin_pos = begin_pos
        self._end_pos = self._begin_pos + self._length
        self._wave_speed = wave_speed
        self._max_window_size = ceil(self._length / self._wave_speed) * 1000

        logging.info(f"Segment {start.id} -- {end.id} created.")

    # TODO:
    # - Liczenie wave_speed dla danego punktu na segmencie pipeline'u.
    def calc_wave_speed(self) -> float:
        return self._wave_speed

    @property
    def max_window_size(self) -> int:
        return self._max_window_size
        

class MethodWave(MethodBase):
    def __init__(self, pipeline: Pipeline, id: int, name: str):
        super().__init__(pipeline, id, name)

        self._get_params()
        self.create_segments()

    def _get_params(self) -> None:
        try:
            self._pressure_deriv_trends = []
            for trend_id in self._params['PRESSURE_DERIV_TRENDS'].split(','):
                self._pressure_deriv_trends.append(self._pipeline.plant.trends[int(trend_id)])
            
            self._max_level = float(self._params['MAX_LEVEL'])
            self._min_level = float(self._params['MIN_LEVEL'])
            self._alarm_level = float(self._params['ALARM_LEVEL'])

            self._wave_speed = float(self._params['BASE_WAVE_SPEED'])

            self._segments: List[Segment] = [] 
            self._length_pipeline = 0
        except KeyError as error:
            if error.args[0] in ('PRESSURE_DERIV_TRENDS', 'MAX_LEVEL', 'MIN_LEVEL', 'ALARM_LEVEL', 'BASE_WAVE_SPEED'):
                logging.exception(f'Param {error.args[0]} does not exist in method {self._id}', exc_info=False)
            else:
                logging.exception(f'Wrong PRESSURE_DERIV_TRENDS value in method {self._id}, trend {error.args[0]} does not exist', exc_info=False)
            raise
    

    def create_segments(self) -> None:
        previous_trend = None
        for current_trend in self._pressure_deriv_trends:
            if (previous_trend is not None):
                segment = Segment(self._pipeline, previous_trend, current_trend,
                                     self._length_pipeline, self._wave_speed)
                self._length_pipeline += segment._length
                self._segments.append(segment)

            previous_trend = current_trend
    
    def get_segment(self, position: int) -> Segment:
        for segment in self._segments:
            if (segment._begin_pos <= position <= segment._end_pos):
                return segment
        return None
    
    def get_probability(self, begin: int, end: int) -> List[List[float]]:
        probability = []
        previous_segment = None
        for current_pos in range(0, int(self._length_pipeline), self._pipeline.length_resolution):
            probability_pos = []
            segment = self.get_segment(current_pos)
            wave_speed = segment.calc_wave_speed()

            if (previous_segment != segment):
                window_begin = begin - segment.max_window_size
                window_end = end + segment.max_window_size
                data_start = segment._start.get_trend_data(window_begin, window_end)
                data_end = segment._end.get_trend_data(window_begin, window_end)

            l1 = current_pos - segment._begin_pos
            l2 = segment._end_pos - current_pos
            offset1 = l1 / wave_speed * 1000 
            offset2 = l2 / wave_speed * 1000

            for current_time in range(begin, end, self._pipeline.time_resolution):
                data_point = current_time - window_begin
                dp1 = min(0, data_start[int((data_point - offset1) / 10)])
                dp2 = min(0, data_end[int((data_point - offset2) / 10)])
                dp3 = min(0, data_start[int((data_point + offset1) / 10)])
                dp4 = min(0, data_end[int((data_point + offset2) / 10)])
                
                res = dp1 + dp2 - dp3 - dp4
                
                res = (res - self._min_level) / (self._max_level - self._min_level)

                res = min(max(0, res), 1)

                probability_pos.append(res)

            previous_segment = segment
            probability.append(probability_pos)

        return probability

    #TODO:
    # Zmienić na wiele segmentów.
    def find_leaks_in_range(self, begin: int, end: int) -> List[Event]:
        events = []
        leak_size = 5
        leak_points = []
        probabilities = self.get_probability(begin, end)

        for position in range(len(probabilities)):
            is_leak = False
            for time in range(len(probabilities[0])):
                if probabilities[position][time] > self._alarm_level:
                    if not is_leak:
                        is_leak = True
                        while (time >= 0 and probabilities[position][time] > 0):
                            time -= 1
                        time += 1
                        leak_points.append((time, position))
                else:
                    is_leak = False

        leak_points.sort()
        leaks = []

        previous_point_id = None
        previous_break_point = 0

        for point_id in range(len(leak_points)):
            if (previous_point_id is not None):
                if (leak_points[point_id][0] - leak_points[previous_point_id][0] > leak_size):
                    leaks.append(leak_points[previous_break_point:point_id])
                    previous_break_point = point_id
            previous_point_id = point_id

        for leak in leaks:
            p = np.polyfit(list(map(lambda x: x[1], leak)), list(map(lambda x: x[0], leak)), deg=10)
            x = np.arange(0, self._length_pipeline, self._pipeline.length_resolution)
            poly = np.poly1d(p)
            y = poly(x)
            leak_length = np.argmax(y)
            leak_time = np.max(y)

            if (0 <= leak_length < len(probabilities) and 0 <= leak_time < len(probabilities[0])):
                events.append(Event(self._id, begin + leak_time * self._pipeline.time_resolution, leak_length * self._pipeline.length_resolution))
        
        #global_plot.probability_heatmap(probabilities, begin, end, self._pipeline.length_resolution)

        return events


    def find_leaks_to(self, end: int) -> List[Event]:
        pass