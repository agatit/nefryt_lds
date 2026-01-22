import logging
import numpy as np
from .base import MethodSegments, Segment
from ..detector_display import DetectorDisplay
from ..event import Event
from ..plant import Pipeline

logger = logging.getLogger(__name__)


class MethodWave(MethodSegments):
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        super().__init__(pipeline, id_, name)
        self._get_params()
        self.displayer = DetectorDisplay()
        self._calculate_params()

    def _get_params(self) -> None:
        try:
            super()._get_params()
            self._leakage_level = float(self._params['LEAKAGE_LEVEL'])
            self._alarm_level = float(self._params['ALARM_LEVEL'])
            self._wave_coeff = float(self._params['WAVE_COEFF'])
            self._normal_range = float(self._params['NORMAL_RANGE'])
            self._no_detection_window = float(self._params['NO_DETECTION_WINDOW']) * 1000
            self._min_wave_value = float(self._params['MIN_WAVE_VALUE'])
            self._read_past_data = bool(self._params.get('READ_PAST_DATA', '1'))
        except KeyError as error:
            raise ValueError(f'{self.__class__.__name__} ({self.id}): No {error.args[0]} param')
        self._create_segments(True)


    def _calculate_params(self):
        self._backtrace_position_delta = int(((self._wave_speed * (self._pipeline.time_resolution / 1000)) * 1.5)
                                             // self.pipeline.length_resolution + 1)
        max_segment_length = max([segment.length for segment in self._segments])
        self._leakage_alarm_delta = int(max_segment_length // self._wave_speed + 1) * 1000
        self._max_trend_time_delta = max(self._trends, key=lambda trend: trend.lds_trend.TimeDelta).lds_trend.TimeDelta
        self._pipeline_flow_time = int((2*(self._pipeline_length / self._wave_speed)+1) * 1000)

    def get_leakage_alarm_delta(self) -> int:
        return self._leakage_alarm_delta

    def get_max_trend_time_delta(self) -> int:
        return self._max_trend_time_delta

    def get_probability(self, segment: Segment, begin: int, end: int) -> np.ndarray:
        window_begin = begin - segment.max_window_size[0]
        window_end = end + segment.max_window_size[1]

        data_start = segment.start.get_trend_data(window_begin, window_end, self._min_wave_value)
        data_end = segment.end.get_trend_data(window_begin, window_end, self._min_wave_value)

        data_start = self._find_waves(data_start, window_begin, True)
        data_end = self._find_waves(data_end, window_begin, True)

        start_pos = round(self.pipeline.length_resolution - ((segment.begin_pos - self.pipeline.begin_pos) % self.pipeline.length_resolution), 0) % self.pipeline.length_resolution
        time = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        position = np.arange(int(start_pos), segment.length, self._pipeline.length_resolution)
        positions, times = np.meshgrid(position, time)

        offset_left_dist = segment.dist_to_start + position
        offset_right_dist = segment.dist_to_end + segment.length - position
        wave_fading_left = np.exp(self._wave_coeff * offset_left_dist).reshape(1, -1)
        wave_fading_right = np.exp(self._wave_coeff * offset_right_dist).reshape(1, -1)

        offset_left = (positions+segment.dist_to_start) / self._wave_speed * 1000
        offset_right = (segment.dist_to_end + segment.length - positions) / self._wave_speed * 1000

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
        self._delete_method_data_from_db()
        begin += (self.pipeline.plant.max_leakage_alarm_delta - self._leakage_alarm_delta)
        events = []
        traces_by_segment = []
        self.displayer = DetectorDisplay()
        for segment in self._segments:
            alarm_start_time = (self.pipeline.plant.max_leakage_alarm_delta - self._leakage_alarm_delta) // self._pipeline.time_resolution
            leakage_start_time = 0
            probability = self.get_probability(segment, begin, end)
            start_pos = round(self.pipeline.length_resolution - (
                        (segment.begin_pos - self.pipeline.begin_pos) % self.pipeline.length_resolution),
                              0) % self.pipeline.length_resolution
            self._save_method_data(probability[alarm_start_time + self._leakage_alarm_delta // self._pipeline.time_resolution:],
                                   range(begin+self._leakage_alarm_delta, end, self._pipeline.time_resolution),
                                   range(int(round(segment.begin_pos + start_pos, 0)), int(segment.end_pos), self._pipeline.length_resolution))
            traces = []
            if segment.no_detection_time - begin > alarm_start_time:
                alarm_start_time = int((segment.no_detection_time - begin) // self._pipeline.time_resolution)
                leakage_start_time = alarm_start_time
            while alarm_start_time < probability.shape[0]:
                trace = self._generate_trace(probability, alarm_start_time, leakage_start_time)
                if trace:
                    if trace[-1][0] > probability.shape[0] - self._leakage_alarm_delta // self._pipeline.time_resolution:
                        break
                    traces.append(trace)
                    alarm_time = trace[0][0]
                    leakage_time = trace[-1][0] * self._pipeline.time_resolution
                    leakage_position = trace[-1][1]
                    events.append(Event(self._id, begin + leakage_time,
                                        segment.begin_pos + start_pos + leakage_position * self._pipeline.length_resolution))
                    alarm_probability = np.where(probability > self._alarm_level, 1, 0)
                    alarm_possibilities_per_time = np.sum(alarm_probability, axis=1)[alarm_time:]
                    no_alarm_times = np.where(alarm_possibilities_per_time == 0)[0]
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
            self.displayer.display(segment_number, 0.4, traces_by_segment[segment_number])
        if len(events) > 0:
            for segment in self._segments:
                segment.no_detection_time = events[-1].time + self._no_detection_window
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
