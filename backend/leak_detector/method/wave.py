import logging
from math import ceil
from typing import List
import numpy as np
from ..tests.plots import global_plot

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
    def __init__(self, pipeline: Pipeline, id: int, name: str) -> None:
        super().__init__(pipeline, id, name)
        self._get_params()
        self._create_segments()

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

    def _create_segments(self) -> None:
        previous_trend = None
        for current_trend in self._pressure_deriv_trends:
            if (previous_trend is not None):
                segment = Segment(self._pipeline, previous_trend, current_trend,
                                     self._length_pipeline, self._wave_speed)
                self._length_pipeline += segment._length
                self._segments.append(segment)

            previous_trend = current_trend
    
    # Wersja dla jednego segmentu:
    def get_probability(self, begin: int, end: int):
        segment = self._segments[0]
        wave_speed = self._wave_speed

        window_begin = begin - segment.max_window_size
        window_end = end + segment.max_window_size

        data_start = segment._start.get_trend_data(window_begin, window_end)
        data_end = segment._end.get_trend_data(window_begin, window_end)
       
        time = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        position = np.arange(0, self._length_pipeline, self._pipeline.length_resolution)
        
        times, positions = np.meshgrid(time, position)

        offset_left = positions / wave_speed * 1000
        offset_right = (self._length_pipeline - positions) / wave_speed * 1000
        
        dp1 = np.array(data_start)[((times - offset_left) / 10).astype(int)]
        dp2 = np.array(data_end)[((times - offset_right) / 10).astype(int)]
        dp3 = np.array(data_start)[((times + offset_left) / 10).astype(int)]
        dp4 = np.array(data_end)[((times + offset_right) / 10).astype(int)]

        dp1 = dp1 * (dp1 < 0) / self._max_level
        dp2 = dp2 * (dp2 < 0) / self._max_level
        dp3 = dp3 * (dp3 < 0) / self._max_level
        dp4 = dp4 * (dp4 < 0) / self._max_level

        probability = np.sqrt(dp1 * dp2)

        global_plot.probability_heatmap(probability, time, position)

        return probability

    #TODO:
    # Zmienić na wiele segmentów.
    def find_leaks_in_range(self, begin: int, end: int) -> List[Event]:
        self.get_probability(begin, end)
        events = []
        return events


    def find_leaks_to(self, end: int) -> List[Event]:
        pass