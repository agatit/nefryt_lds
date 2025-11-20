import logging
import numpy as np
from scipy.interpolate import interp1d
from .base import MethodBase, Segment
from ..detector_display import detector_display
from ..event import Event
from ..leak import Leakage
from ..plant import Pipeline, Trend


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
            self._leakage_window = float(self._params['LEAKAGE_WINDOW'])
            self._no_detection_window = float(self._params['NO_DETECTION_WINDOW'])
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
        self._pipeline_length = self._pipeline.begin_pos
        previous_trend = None
        for current_trend in self._pressure_deriv_trends:
            if previous_trend is not None:
                segment = Segment(self._pipeline, previous_trend, current_trend,
                                     self._pipeline_length, self._wave_speed)
                self._pipeline_length += segment.length
                self._segments.append(segment)
            previous_trend = current_trend

    def get_probability(self, segment: Segment, begin: int, end: int) -> np.ndarray:
        pass

    # TODO: multiple checks in one window
    def find_leaks_in_range(self, begin: int, end: int) -> list[Event]:
        events = []
        segment_leakage_times: dict[Segment, tuple] = dict()
        for segment in self._segments:
            probability = self.get_probability(segment, begin, end)
            leakage_probability = np.where(probability > self._alarm_level, 1, 0).T
            if segment.no_detection_time is not None:
                if segment.current_detection_end_time is not None:
                    end_time = int((segment.current_detection_end_time - begin) // self._pipeline.time_resolution) \
                        if segment.current_detection_end_time < end else -1
                    max_position, max_time = np.unravel_index(np.argmax(probability[:, :end_time]), probability[:, :end_time].shape)
                    max_probability = probability[max_position, int(max_time)]
                    leakage = Leakage(float(max_probability), int(max_position), begin+int(max_time)*self._pipeline.time_resolution)
                    if leakage.probability > segment.current_leakage.probability:
                        segment.current_leakage = leakage
                    if segment.current_detection_end_time < end:
                        events.append(Event(self._id,
                                            segment.current_leakage.timestamp,
                                            segment.begin_pos - self._pipeline.begin_pos + segment.current_leakage.position * self._pipeline.length_resolution,
                                            segment.current_leakage.probability))
                        segment.current_leakage = None
                        segment.current_detection_end_time = None

                if segment.no_detection_time > end:
                    continue
                else:
                    end_time = int((segment.no_detection_time - begin) // self._pipeline.time_resolution)
                    segment.no_detection_time = None
                    leakage_probability[:end_time] = 0
            leaks = np.argwhere(leakage_probability == 1)
            if len(leaks) > 0:
                first_time, _ = leaks[0]
                end_time = int(first_time+self._leakage_window//10) if first_time+self._leakage_window//10 < probability.shape[1] else -1
                max_position, max_time = np.unravel_index(np.argmax(probability[:, first_time:end_time]), probability[:, first_time:end_time].shape)
                max_probability = probability[max_position, first_time+int(max_time)]
                leakage = Leakage(float(max_probability), int(max_position), begin+(first_time+int(max_time))*self._pipeline.time_resolution)
                segment_leakage_times[segment] = (first_time, leakage)

        if len(segment_leakage_times) > 0:
            leakage_segment = min(segment_leakage_times, key=lambda k: segment_leakage_times[k][0])
            first_leakage_time, leakage = segment_leakage_times[leakage_segment]
            if begin + first_leakage_time  * self._pipeline.time_resolution + self._leakage_window >= end:
                leakage_segment.current_leakage = leakage
                leakage_segment.current_detection_end_time = begin + first_leakage_time  * self._pipeline.time_resolution + self._leakage_window
            else:
                events.append(Event(self._id,
                                    leakage.timestamp,
                                    leakage_segment.begin_pos - self._pipeline.begin_pos + leakage.position * self._pipeline.length_resolution,
                                    leakage.probability))

            for segment in self._segments:
                segment.no_detection_time = begin + first_leakage_time*self._pipeline.time_resolution + self._no_detection_window

        return events

    def find_leaks_to(self, end: int) -> list[Event]:
        pass


class MethodWaveSigned(MethodWave):
    def get_probability(self, segment: Segment, begin: int, end: int) -> np.ndarray:
        window_begin = begin - segment.max_window_size
        window_end = end + segment.max_window_size

        data_start = segment.start.get_trend_data(window_begin, window_end)
        data_end = segment.end.get_trend_data(window_begin, window_end)

        time = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        position = np.arange(0, segment.length, self._pipeline.length_resolution)
        positions, times = np.meshgrid(position, time)

        # past_delay = 2 * int(1000*self._pipeline_length / self._wave_speed)
        # past_window_begin = window_begin - past_delay
        # past_window_end = window_end - past_delay
        #
        # past_data_start = segment.start.get_trend_data(past_window_begin, past_window_end, 10)
        # past_data_end = segment.end.get_trend_data(past_window_begin, past_window_end, 10)
        # interp_func_start = interp1d(np.arange(0, len(data_start)+1, 10), past_data_start,
        #                              kind='linear', bounds_error=False, fill_value=0)
        # interp_func_end = interp1d(np.arange(0, len(data_end)+1, 10), past_data_end,
        #                            kind='linear', bounds_error=False, fill_value=0)
        #
        # past_data_start = interp_func_start(np.arange(len(data_start)))
        # past_data_end = interp_func_end(np.arange(len(data_end)))
        # past_data_wave_fading = np.exp(self._wave_coeff * self._pipeline_length)
        # data_start_subtracted = data_start - past_data_start / past_data_wave_fading
        # data_end_subtracted = data_end - past_data_end / past_data_wave_fading

        # dp1 = np.array(data_start_subtracted)[dp1_indexes] / (self._normal_range * wave_fading_left)
        # dp2 = np.array(data_end_subtracted)[dp2_indexes] / (self._normal_range * wave_fading_right)
        # dp3 = np.array(data_start_subtracted)[dp3_indexes] / (self._normal_range * wave_fading_left)
        # dp4 = np.array(data_end_subtracted)[dp4_indexes] / (self._normal_range * wave_fading_right)

        offset_left_dist = position
        offset_right_dist = segment.length - position
        wave_fading_left = np.exp(self._wave_coeff * offset_left_dist).reshape(1, -1)
        wave_fading_right = np.exp(self._wave_coeff * offset_right_dist).reshape(1, -1)

        offset_left = positions / self._wave_speed * 1000
        offset_right = (segment.length - positions) / self._wave_speed * 1000

        dp1_indexes = ((times - offset_left) / 10).astype(int)
        dp2_indexes = ((times - offset_right) / 10).astype(int)
        dp3_indexes = ((times + offset_left) / 10).astype(int)
        dp4_indexes = ((times + offset_right) / 10).astype(int)

        dp1 = np.array(data_start)[dp1_indexes] / (self._normal_range * wave_fading_left)
        dp2 = np.array(data_end)[dp2_indexes] / (self._normal_range * wave_fading_right)
        dp3 = np.array(data_start)[dp3_indexes] / (self._normal_range * wave_fading_left)
        dp4 = np.array(data_end)[dp4_indexes] / (self._normal_range * wave_fading_right)

        # TODO: if wave value < N => set it to zero
        probability_start = np.maximum(dp1 - dp4, 0)
        probability_end = np.maximum(dp2 - dp3, 0)
        probability = probability_start * probability_end
        probability = np.sqrt(np.maximum(probability, 0))
        probability = np.minimum(probability, 1)
        detector_display(self, True, segment, begin, end, probability, data_start, data_end,
                      [dp1_indexes, dp2_indexes, dp3_indexes, dp4_indexes])

        return probability

class MethodWaveUnsigned(MethodWave):
    def get_probability(self, segment: Segment, begin: int, end: int) -> np.ndarray:
        window_begin = begin - segment.max_window_size
        window_end = end + segment.max_window_size

        data_start = np.abs(segment.start.get_trend_data(window_begin, window_end))
        data_end = np.abs(segment.end.get_trend_data(window_begin, window_end))

        past_delay = int(1000*self._pipeline_length / self._wave_speed)
        past_window_begin = window_begin - past_delay
        past_window_end = window_end - past_delay

        past_data_start = segment.start.get_trend_data(past_window_begin, past_window_end, 10)
        past_data_end = segment.end.get_trend_data(past_window_begin, past_window_end, 10)
        interp_func_start = interp1d(np.arange(0, len(data_start)+1, 10), past_data_start,
                                     kind='linear', bounds_error=False, fill_value=0)
        interp_func_end = interp1d(np.arange(0, len(data_end)+1, 10), past_data_end,
                                   kind='linear', bounds_error=False, fill_value=0)

        past_data_start = np.abs(interp_func_start(np.arange(len(data_start))))
        past_data_end = np.abs(interp_func_end(np.arange(len(data_end))))
        past_data_wave_fading = np.exp(self._wave_coeff * self._pipeline_length)
        data_start = data_start - past_data_start / past_data_wave_fading
        data_end = data_end - past_data_end / past_data_wave_fading

        time = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        position = np.arange(0, segment.length, self._pipeline.length_resolution)

        offset_left_dist = position
        offset_right_dist = segment.length - position
        wave_fading_left = np.exp(self._wave_coeff * offset_left_dist).reshape(-1, 1)
        wave_fading_right = np.exp(self._wave_coeff * offset_right_dist).reshape(-1, 1)

        times, positions = np.meshgrid(time, position)

        offset_left = positions / self._wave_speed * 1000
        offset_right = (segment.length - positions) / self._wave_speed * 1000

        dp1_indexes = ((times - offset_left) / 10).astype(int)
        dp2_indexes = ((times - offset_right) / 10).astype(int)
        dp3_indexes = ((times + offset_left) / 10).astype(int)
        dp4_indexes = ((times + offset_right) / 10).astype(int)

        dp1 = np.abs(np.array(data_start))[dp1_indexes] / (self._normal_range * wave_fading_left)
        dp2 = np.abs(np.array(data_end))[dp2_indexes] / (self._normal_range * wave_fading_right)
        dp3 = np.abs(np.array(data_start))[dp3_indexes] / (self._normal_range * wave_fading_left)
        dp4 = np.abs(np.array(data_end))[dp4_indexes] / (self._normal_range * wave_fading_right)

        probability_start = np.maximum(dp1 - dp4, 0)
        probability_end = np.maximum(dp2 - dp3, 0)
        probability = probability_start * probability_end
        probability = np.sqrt(np.maximum(probability, 0))
        probability = np.minimum(probability, 1)

        detector_display(self, True, segment, begin, end, probability, data_start, data_end,
                      [dp1_indexes, dp2_indexes, dp3_indexes, dp4_indexes],)

        return probability
