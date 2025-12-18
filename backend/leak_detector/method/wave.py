import logging
import numpy as np
from .base import MethodBase, Segment
from ..detector_display import DetectorDisplay
from ..event import Event
from ..plant import Pipeline, Trend


class MethodWave(MethodBase):
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        super().__init__(pipeline, id_, name)
        self._get_params()
        self._begin_pos = pipeline.plant.get_distances(pipeline.first_node, self._pipeline.plant.nodes[self._trends[0].node_id])[0]
        self.displayer = DetectorDisplay()
        self._calculate_params()
        self._stored_events = []

    def _get_params(self) -> None:
        try:
            self._pressure_deriv_trend_ids  = str(self._params['PRESSURE_DERIV_TRENDS']).split(',')
            self._leakage_level = float(self._params['LEAKAGE_LEVEL'])
            self._alarm_level = float(self._params['ALARM_LEVEL'])
            self._wave_speed = float(self._params['BASE_WAVE_SPEED'])
            self._wave_coeff = float(self._params['WAVE_COEFF'])
            self._normal_range = float(self._params['NORMAL_RANGE'])
            self._no_detection_window = float(self._params['NO_DETECTION_WINDOW_SECONDS']) * 1000
            self._min_wave_value = float(self._params['MIN_WAVE_VALUE'])
            self._read_past_data = bool(self._params.get('READ_PAST_DATA', '1'))
        except KeyError as error:
            logging.exception(f'Param {error.args[0]} does not exist in method {self._id}', exc_info=False)
            raise

        try:
            self._trends : list[Trend] = []
            for trend_id in self._pressure_deriv_trend_ids:
                self._trends.append(self._pipeline.plant.trends[int(trend_id)])
        except KeyError as error:
            logging.exception(f'Wrong PRESSURE_DERIV_TRENDS value in method {self._id}, '
                              f'trend {error.args[0]} does not exist', exc_info=False)
            raise

        self._create_segments()

    def _create_segments(self) -> None:
        self._segments: list[Segment] = []
        self._pipeline_length = self._pipeline.begin_pos
        previous_trend = None
        for current_trend in self._trends:
            if previous_trend is not None:
                segment = Segment(self._pipeline, previous_trend, current_trend,
                                     self._pipeline_length, self._wave_speed)
                self._pipeline_length += segment.length
                self._segments.append(segment)
            previous_trend = current_trend

    def _calculate_params(self):
        self._backtrace_position_delta = int(((self._wave_speed * (self._pipeline.time_resolution / 1000)) * 1.5)
                                             // self.pipeline.length_resolution + 1)
        max_segment_length = max([segment.length for segment in self._segments])
        self._leakage_alarm_delta = int(max_segment_length // self._wave_speed + 1) * 1000
        self._pipeline_flow_time = int((2*(self._pipeline_length / self._wave_speed)+1) * 1000)

    def get_leakage_alarm_delta(self) -> int:
        return self._leakage_alarm_delta

    def get_probability(self, segment: Segment, begin: int, end: int) -> np.ndarray:
        pass

    def _generate_alarms(self, probability_part: np.ndarray) -> list:
        alarm_probability = np.where(probability_part > self._alarm_level, 1, 0)
        alarms = np.argwhere(alarm_probability == 1)
        if len(alarms) > 0:
            alarm_times = np.unique(alarms[:, 0])
            return alarm_times.tolist()
        else:
            return []

    def _generate_trace(self, probability: np.ndarray, alarm_start_time: int, leakage_start_time: int) -> list | None:
        probability_part = probability[alarm_start_time:]
        alarm_times = self._generate_alarms(probability_part)
        if len(alarm_times) > 0:
            alarm_time = alarm_times[0]
            previous_alarm_time = alarm_time - 1
            while alarm_time - previous_alarm_time == 1:
                alarms_in_time = np.count_nonzero(probability_part[alarm_time] > self._alarm_level)
                sorted_alarm_positions = np.argsort(probability_part[alarm_time])[::-1][:alarms_in_time]
                for alarm_position in sorted_alarm_positions:
                    current_time = alarm_time
                    current_position = alarm_position
                    trace = [(alarm_start_time + current_time, current_position)]

                    while alarm_start_time+current_time > leakage_start_time:
                        current_time -= 1
                        position_min = max(0, current_position - self._backtrace_position_delta)
                        position_max = min(probability.shape[1], current_position + self._backtrace_position_delta + 1)
                        window = probability[alarm_start_time+current_time, position_min:position_max]

                        if np.all(window <= self._leakage_level):
                            break

                        max_level_position_in_window = int(np.argmax(window))
                        current_position = position_min + max_level_position_in_window
                        trace.append((alarm_start_time + current_time, current_position))
                    return trace
        return None

    def find_leaks_in_range(self, begin: int, end: int) -> list[Event]:
        events = []
        traces_by_segment = []
        self.displayer = DetectorDisplay()
        for segment in self._segments:
            alarm_start_time = self._pipeline.plant.get_leakage_alarm_delta() // self._pipeline.time_resolution
            leakage_start_time = 0
            traces = []
            if segment.no_detection_time - begin > alarm_start_time:
                alarm_start_time = int((segment.no_detection_time - begin) // self._pipeline.time_resolution)
                leakage_start_time = alarm_start_time
            probability = self.get_probability(segment, begin, end)
            while alarm_start_time < probability.shape[0]:
                trace = self._generate_trace(probability, alarm_start_time, leakage_start_time)
                if trace:
                    traces.append(trace)
                    alarm_time = trace[0][0]
                    leakage_time = trace[-1][0] * self._pipeline.time_resolution
                    leakage_position = trace[-1][1]
                    events.append(Event(self._id, begin + leakage_time,
                                        segment.begin_pos - self._pipeline.begin_pos + leakage_position * self._pipeline.length_resolution))
                    alarm_probability = np.where(probability > self._alarm_level, 1, 0)
                    alarm_possibilities_per_time = np.sum(alarm_probability, axis=1)[alarm_time:]
                    no_alarm_times = np.where(alarm_possibilities_per_time == 0)[0]
                    segment.no_detection_time = begin + alarm_time * self._pipeline.time_resolution + self._no_detection_window
                    if len(no_alarm_times) == 0:
                        break
                    no_detection_time = no_alarm_times[0] \
                        if no_alarm_times[0] > self._no_detection_window // self._pipeline.time_resolution \
                        else self._no_detection_window // self._pipeline.time_resolution
                    alarm_start_time = int(no_detection_time + alarm_time)
                    leakage_start_time = alarm_start_time
                else:
                    break

            traces_by_segment.append(traces)

        events, traces_by_segment = self.choose_events(events, traces_by_segment, begin)
        for segment_number in range(len(self._segments)):
            self.displayer.display(segment_number, 0.15, traces_by_segment[segment_number])
        return events

    def choose_events(self, events: list, traces_by_segment: list, begin: int):
        traces = []
        return_traces = []
        for i, segment_traces in enumerate(traces_by_segment):
            traces.extend([(i, trace) for trace in segment_traces])
            return_traces.append([])
        for event, trace in sorted(zip(events, traces), key=lambda o: o[0].time):
            if len(self._stored_events) == 0 or event.time - self._stored_events[-1].time > self._pipeline_flow_time:
                self._stored_events.append(event)
                segment_no, trace = trace
                return_traces[segment_no].append(trace)
        self._stored_events = [event for event in self._stored_events if begin - event.time < self._pipeline_flow_time]
        return [event for event in self._stored_events if event.time >= begin], return_traces

    def find_leaks_to(self, end: int) -> list[Event]:
        pass


class MethodWaveSigned(MethodWave):
    def get_probability(self, segment: Segment, begin: int, end: int) -> np.ndarray:
        window_begin = begin - segment.max_window_size[0]
        window_end = end + segment.max_window_size[1]

        # To remove multiple detections of the same wave & find where leakages overlap:
        # - find previous high / low peak in around ~2*pipeline.flow_time
        # - check whether shape of the peak is identical as current peak
        # - if yes: discard, if not: detect
        data_start = segment.start.get_trend_data(window_begin, window_end, self._min_wave_value)
        data_end = segment.end.get_trend_data(window_begin, window_end, self._min_wave_value)

        time = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        position = np.arange(0, segment.length, self._pipeline.length_resolution)
        positions, times = np.meshgrid(position, time)

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

        probability_start = np.maximum(dp1 - dp4, 0)
        probability_end = np.maximum(dp2 - dp3, 0)
        probability = probability_start * probability_end
        probability = np.sqrt(np.maximum(probability, 0))
        probability = np.minimum(probability, 1)
        self.displayer.set_params(data_start, data_end, [dp1_indexes, dp2_indexes, dp3_indexes, dp4_indexes],
                                  self, segment, begin, end, probability, None, None, None)

        return probability
