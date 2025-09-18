import logging
import numpy as np
from scipy.ndimage import label
from .base import MethodBase, Segment
from ..plant import Event, Pipeline, Trend


# Every segment have the same, const wave speed
class MethodWave(MethodBase):
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        super().__init__(pipeline, id_, name)
        self._get_params()
        self._create_segments()
        self._begin_pos = pipeline.plant.get_distances(pipeline.first_node,
                                                       self._pipeline.plant.nodes[self._pressure_deriv_trends[0].node_id])[0]

    def _get_params(self) -> None:
        try:
            self._pressure_deriv_trend_ids  = str(self._params['PRESSURE_DERIV_TRENDS']).split(',')
            self._min_level = float(self._params['MIN_LEVEL'])
            self._alarm_level = float(self._params['ALARM_LEVEL'])
            self._wave_speed = float(self._params['BASE_WAVE_SPEED'])
            self._wave_coeff = float(self._params['WAVE_COEFF'])
            self._normal_range = float(self._params['NORMAL_RANGE'])
        except KeyError as error:
            logging.exception(f'Param {error.args[0]} does not exist in method {self._id}', exc_info=False)
            raise

        try:
            self._pressure_deriv_trends : list[Trend] = []
            for trend_id in self._pressure_deriv_trend_ids:
                self._pressure_deriv_trends.append(self._pipeline.plant.trends[int(trend_id)])
        except KeyError as error:
            logging.exception(f'Wrong PRESSURE_DERIV_TRENDS value in method {self._id}, '
                              f'trend {error.args[0]} does not exist', exc_info=False)
            raise

    def _create_segments(self) -> None:
        self._segments: list[Segment] = []
        self._length_pipeline = 0
        previous_trend = None
        for current_trend in self._pressure_deriv_trends:
            if previous_trend is not None:
                segment = Segment(self._pipeline, previous_trend, current_trend,
                                     self._length_pipeline, self._wave_speed)
                self._length_pipeline += segment.length
                self._segments.append(segment)

            previous_trend = current_trend
    
    def get_probability(self, segment: Segment, begin: int, end: int) -> list[list[float]]:
        wave_speed = self._wave_speed
        # print(f'Wave speed: {wave_speed}')

        window_begin = begin - segment.max_window_size
        # print(f'Window begin: {window_begin}')

        window_end = end + segment.max_window_size
        # print(f'Window end: {window_end}')

        # print(f'Diff: {window_end - window_begin}')
        data_start = segment.start.get_trend_data(window_begin, window_end)
        # print(f'Data start: {len(data_start)} {min(data_start)} {max(data_start)}')
        data_end = segment.end.get_trend_data(window_begin, window_end)
        # print(f'Data end: {len(data_end)} {min(data_end)} {max(data_end)}')

        times = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        # print(f'Times: {times}')
        positions = np.arange(0, segment.length, self._pipeline.length_resolution)
        # print(f'Positions: {positions}')
        
        times, positions = np.meshgrid(times, positions)
        # print(f'Times: {times}')
        # print(f'Positions: {positions}')

        offset_left = positions / wave_speed * 1000
        # print(f'Offset left: {offset_left}')
        offset_right = (segment.length - positions) / wave_speed * 1000
        # print(f'Offset right: {offset_right}')
        
        wave_fading = (1 - self._wave_coeff * positions / segment.length) \
                    * (1 - self._wave_coeff * (1 - positions / segment.length))

        # print(f'Wave fading: {wave_fading}')
        # print(f'Minus: {((times - offset_right) / 10).astype(int)}')
        # print(f'Plus: {((times + offset_right) / 10).astype(int)}')
        dp1 = np.array(data_start)[((times - offset_left) / 10).astype(int)] / self._normal_range
        dp2 = np.array(data_end)[((times - offset_right) / 10).astype(int)] / self._normal_range
        dp3 = np.array(data_start)[((times + offset_left) / 10).astype(int)] / self._normal_range
        dp4 = np.array(data_end)[((times + offset_right) / 10).astype(int)] / self._normal_range

        # print(f'dp1: {dp1}')
        # print(f'dp2: {dp2}')
        # print(f'dp3: {dp3}')
        # print(f'dp4: {dp4}')

        probability = dp3 * dp4 - dp1 * dp2
        print(np.min(probability))
        print(np.max(probability))

        probability = np.maximum(probability, 0)
        # print(probability)

        probability = np.where(wave_fading > 0, np.sqrt(probability / wave_fading), 0)
        print(np.min(probability))
        print(np.max(probability))

        print('===========================')

        probability = np.minimum(probability, 1)
        # print(probability)

        return probability

    def find_leaks_in_range(self, begin: int, end: int) -> list[Event]:
        events = []
        for segment in self._segments:
            probability = self.get_probability(segment, begin, end)

            leaks, _ = label(probability > 0)

            probability = np.where(probability > self._min_level, probability, 0)

            alarm_labels = np.unique(np.where(probability > self._alarm_level, leaks, 0))[1:]

            for alarm_label in alarm_labels:
                alarm_values = np.where(leaks == alarm_label, probability, 0)
                alarm_point_time = np.argmin(np.sum(alarm_values, axis=0) == 0)
                alarm_point_position = np.mean(np.nonzero(alarm_values[:,alarm_point_time])) # or np.min, np.max, np.median etc.
                alarm_time = begin + self._pipeline.time_resolution * alarm_point_time
                alarm_position = self._pipeline.length_resolution * alarm_point_position
                events.append(Event(self._id, alarm_time, self._begin_pos + segment.begin_pos + alarm_position))
                
        return events

    def find_leaks_to(self, end: int) -> list[Event]:
        pass
