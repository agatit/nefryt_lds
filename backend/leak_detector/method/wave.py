import logging
from typing import List
import numpy as np
from ..tests.plots import global_plot
from scipy.ndimage import label

from .base import MethodBase, Segment
from ..plant import Event, Pipeline, Trend

# Obecna wersja zakłada, że segmenty mają stały wave speed.
class MethodWave(MethodBase):
    def __init__(self, pipeline: Pipeline, id: int, name: str) -> None:
        super().__init__(pipeline, id, name)        
        self._get_params()
        self._create_segments()
        self._begin_pos = pipeline.plant.get_distances(pipeline._first_node, self._pipeline.plant.nodes[self._pressure_deriv_trends[0].node_id])[0]

    def _get_params(self) -> None:
        try:
            self._pressure_derivs_string = str(self._params['PRESSURE_DERIV_TRENDS'])

            self._min_level = float(self._params['MIN_LEVEL'])
            self._max_level = float(self._params['MAX_LEVEL'])
            self._alarm_level = float(self._params['ALARM_LEVEL'])

            self._wave_speed = float(self._params['BASE_WAVE_SPEED'])

            self._wave_coeff = float(self._params['WAVE_COEFF'])

            self._normal_range = float(self._params['NORMAL_RANGE'])
        except KeyError as error:
            logging.exception(f'Param {error.args[0]} does not exist in method {self._id}', exc_info=False)
            raise
        try:
            self._pressure_deriv_trends : List[Trend] = []
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
    
    def get_probability(self, segment: Segment, begin: int, end: int):
        wave_speed = self._wave_speed

        window_begin = begin - segment.max_window_size
        window_end = end + segment.max_window_size

        data_start = segment._start.get_trend_data(window_begin, window_end)
        data_end = segment._end.get_trend_data(window_begin, window_end)
       
        time = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        position = np.arange(0, segment._length, self._pipeline.length_resolution)
        
        times, positions = np.meshgrid(time, position)

        offset_left = positions / wave_speed * 1000
        offset_right = (segment._length - positions) / wave_speed * 1000
        
        friction = (1 - self._wave_coeff * positions / segment._length) \
                    * (1 - self._wave_coeff * (1 - positions / segment._length))

        dp1 = np.array(data_start)[((times - offset_left) / 10).astype(int)] / self._normal_range
        dp2 = np.array(data_end)[((times - offset_right) / 10).astype(int)] / self._normal_range
        dp3 = np.array(data_start)[((times + offset_left) / 10).astype(int)] / self._normal_range
        dp4 = np.array(data_end)[((times + offset_right) / 10).astype(int)] / self._normal_range

        probability = dp3 * dp4 - dp1 * dp2

        probability = np.maximum(probability, 0)

        probability = np.where(friction > 0, np.sqrt(probability / friction), 0)

        probability = np.minimum(probability, 1)

        return probability

    def find_leaks_in_range(self, begin: int, end: int) -> List[Event]:
        events = []

        for segment in self._segments:
            probability = self.get_probability(segment, begin, end)

            leaks, _ = label(probability > 0)

            alarm_labels = np.unique(np.where(probability > self._alarm_level, leaks, 0))[1:]

            for alarm_label in alarm_labels:
                leak_values = np.where(leaks == alarm_label, probability, 0)
                leak_values_from_end = np.flip(leak_values, axis=1)
                is_alarm_after = np.flip(np.logical_or.accumulate(leak_values_from_end > self._alarm_level, axis=1), axis=1)
                is_alarm_after = is_alarm_after * (leak_values > 0)
                alarm_point_time = np.argmin(np.max(leak_values, axis=0) == 0)
                alarm_point_position = np.mean(np.nonzero(leak_values[:, alarm_point_time]))

                alarm_time = begin + self._pipeline.time_resolution * alarm_point_time
                alarm_position = self._pipeline.length_resolution * alarm_point_position
                events.append(Event(self._id, alarm_time, self._begin_pos + segment._begin_pos + alarm_position))

        return events

    def find_leaks_to(self, end: int) -> List[Event]:
        pass