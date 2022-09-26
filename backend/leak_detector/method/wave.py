import logging
from math import ceil
from typing import List
import numpy as np
from ..tests.plots import global_plot
from scipy.ndimage import label

from .base import MethodBase
from ..trend import Trend
from ..plant import Event, Pipeline

# Obecna wersja zakłada, że segmenty mają stały wave speed.
# Może wpakować to jako podklasy Klasy MethodBase?
class Segment:
    def __init__(self, pipeline: Pipeline, start: Trend, end: Trend, begin_pos: int, wave_speed: float) -> None:
        distances = pipeline.plant.get_distances(pipeline.plant.nodes[start.node_id], pipeline.plant.nodes[end.node_id])
        if (len(distances) != 1):
            logging.exception(f"There isn't exactly one path between {start.id} and {end.id}.")
            raise
        self._length = distances[0]
        self._start = start
        self._end = end
        self._begin_pos = begin_pos
        self._end_pos = self._begin_pos + self._length
        self._wave_speed = wave_speed
        self._max_window_size = ceil(self._length / self._wave_speed) * 1000

        logging.debug(f"Segment {start.id} <--> {end.id} created.")

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
            self._pressure_derivs_string = str(self._params['PRESSURE_DERIV_TRENDS'])
            
            self._max_level = float(self._params['MAX_LEVEL'])
            self._min_level = float(self._params['MIN_LEVEL'])
            self._alarm_level = float(self._params['ALARM_LEVEL'])

            self._wave_speed = float(self._params['BASE_WAVE_SPEED'])
        except KeyError as error:
            logging.exception(f'Param {error.args[0]} does not exist in method {self._id}', exc_info=False)
            raise
        try:
            self._pressure_deriv_trends = []
            for trend_id in self._pressure_derivs_string.split(','):
                self._pressure_deriv_trends.append(self._pipeline.plant.trends[int(trend_id)])
        except KeyError as error:
            logging.exception(f'Wrong PRESSURE_DERIV_TRENDS value in method {self._id}, trend {error.args[0]} does not exist', exc_info=False)
            raise

    def _create_segments(self) -> None:
        self._segments: List[Segment] = [] 
        self._length_pipeline = 0
        previous_trend = None
        for current_trend in self._pressure_deriv_trends:
            if (previous_trend is not None):
                segment = Segment(self._pipeline, previous_trend, current_trend,
                                     self._length_pipeline, self._wave_speed)
                self._length_pipeline += segment._length
                self._segments.append(segment)

            previous_trend = current_trend
    
    # Wersja dla jednego segmentu:
    # Usunąć echa
    def get_probability(self, begin: int, end: int):
        scale = 300000 # W Zygmuntowie, pomiary mają różną dokładność, więc skalowanie danych na zakres (0,1),
                       # można zrobić tylko wtedy, gdy dzielimy wartość ciśnienia przez maksymalną wartość pomiaru na obu 
                       # czujnikach w Pa/s.
        d = 0.3 # Przykładowa wartość

        segment = self._segments[0]
        wave_speed = self._wave_speed

        window_begin = begin - segment.max_window_size
        window_end = end + segment.max_window_size

        data_start = segment._start.get_trend_data(window_begin, window_end)
        data_end = segment._end.get_trend_data(window_begin, window_end)
       
        time = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        position = np.arange(0, self._length_pipeline, self._pipeline.length_resolution)
        
        times, positions = np.meshgrid(time, np.flip(position))

        offset_left = positions / wave_speed * 1000
        offset_right = (self._length_pipeline - positions) / wave_speed * 1000
        
        friction = (1 - d * positions / self._length_pipeline) * (1 - d * (1 - positions / self._length_pipeline))

        dp1 = np.array(data_start)[((times - offset_left) / 10).astype(int)]
        dp2 = np.array(data_end)[((times - offset_right) / 10).astype(int)]

        dp1 = - dp1 * (dp1 < 0) / scale
        dp2 = - dp2 * (dp2 < 0) / scale

        probability = np.where(friction > 0, np.sqrt(dp1 * dp2 / friction), 0)

        return probability

    def find_leaks_in_range(self, begin: int, end: int) -> List[Event]:
        probability = self.get_probability(begin, end)

        events = []

        leaks, _ = label(probability > 0)
        alarm_labels = np.unique(np.where(probability > self._alarm_level, leaks, 0))[1:]

        probability = np.where(probability > self._min_level, probability, 0)
        probability = np.where(probability < self._max_level, probability, 1)

        for alarm_label in alarm_labels:
            alarm_values = np.where(leaks == alarm_label, probability, 0)
            # First non-zero point method:
            alarm_point_time = np.argmin(np.sum(alarm_values, axis=0) == 0)
            alarm_point_position = np.min(np.nonzero(alarm_values[:,alarm_point_time])) #ewentualnie np.mean
            alarm_time = begin + self._pipeline.time_resolution * alarm_point_time
            alarm_position = self._pipeline.length_resolution * alarm_point_position
            events.append(Event(self._id, alarm_time, alarm_position))

        return events

    def find_leaks_to(self, end: int) -> List[Event]:
        pass