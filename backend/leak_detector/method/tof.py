import logging
import numpy as np
from .base import MethodBase, Segment
from ..detector_display import DetectorDisplay
from ..event import Event
from ..plant import Pipeline
from ..trend import Trend


class MethodTOF(MethodBase):
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        super().__init__(pipeline, id_, name)
        self._get_params()
        self._create_segments()
        self._begin_pos = pipeline.plant.get_distances(pipeline.first_node, self._pipeline.plant.nodes[self._trends[0].node_id])[0]
        self.displayer = DetectorDisplay()
        self._stored_events = []

    def _get_params(self) -> None:
        try:
            self._pressure_deriv_trend_ids  = str(self._params['PRESSURE_DERIV_TRENDS']).split(',')
            self._drop_level = float(self._params['DROP_LEVEL'])
            self._wave_speed = float(self._params['BASE_WAVE_SPEED'])
            self._wave_speed_sigma = float(self._params['WAVE_SPEED_SIGMA'])
            self._time_sigma = float(self._params['TIME_SIGMA'])
            self._no_detection_window = float(self._params['NO_DETECTION_WINDOW_SECONDS']) * 1000
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

    def _create_segments(self) -> None:
        self._segments: list[Segment] = []
        self._pipeline_length = self._pipeline.begin_pos
        previous_trend = None
        for current_trend in self._trends:
            if previous_trend is not None:
                segment = Segment(self._pipeline, previous_trend, current_trend,
                                     self._pipeline_length, self._wave_speed, (False, True))
                self._pipeline_length += segment.length
                self._segments.append(segment)
            previous_trend = current_trend
        self._pipeline_flow_time = int((2 * (self._pipeline_length / self._wave_speed) + 1) * 1000)

    def simulate_probability(self, positions, peaks, segment_length):
        probability = np.zeros_like(positions)
        n_samples = 100000
        time_sigma = self._time_sigma / self.pipeline.time_resolution
        start_time = 0
        for (peak_start, peak_end) in peaks:
            peaks_diff_t = abs(peak_end - peak_start) * self._pipeline.time_resolution
            wave_speed = np.random.normal(self._wave_speed, self._wave_speed_sigma, n_samples)
            moved_peak_start = peak_start + np.random.normal(0,  time_sigma, n_samples)
            segment_flow_time = (segment_length / wave_speed) * 1000
            diff_t_from_edge = (segment_flow_time - peaks_diff_t) / 2
            diff_t_from_edge[diff_t_from_edge < 0] = 0
            diff_dist_from_edge = (diff_t_from_edge / 1000) * wave_speed
            leakage_position = segment_length - diff_dist_from_edge if peak_start > peak_end else diff_dist_from_edge
            leakage_time = (moved_peak_start * self._pipeline.time_resolution) - segment_flow_time * (leakage_position / segment_length)
            leakage_position_idxs = (leakage_position / self._pipeline.length_resolution).astype(int)
            leakage_time_idxs = (leakage_time / self._pipeline.time_resolution).astype(int)
            for (leakage_time_idx, leakage_position_idx) in zip(leakage_time_idxs.tolist(), leakage_position_idxs.tolist()):
                if 0 <= leakage_time_idx < probability.shape[0] and 0 <= leakage_position_idx < probability.shape[1]:
                    probability[leakage_time_idx, leakage_position_idx] += 1
            probability[start_time:max(leakage_time_idxs)+1] /= probability[start_time:max(leakage_time_idxs)+1].max()
            start_time = max(leakage_time_idxs)+1

        return probability

    def get_probability(self, segment: Segment, begin: int, end: int) -> list[list[float]] | np.ndarray:
        window_begin = begin - segment.max_window_size[0]
        window_end = end + segment.max_window_size[1]

        data_start = segment.start.get_trend_data(window_begin, window_end)
        data_end = segment.end.get_trend_data(window_begin, window_end)

        data_start_wave_idxs = np.nonzero(-data_start >= self._drop_level)[0]
        data_start_wave_idxs = np.insert(data_start_wave_idxs, 0, -1, axis=0)
        data_start_peaks_idxs = data_start_wave_idxs[np.nonzero(np.diff(data_start_wave_idxs) > 1)[0] + 1] # TODO: change 1 to some parametrized value

        data_end_wave_idxs = np.nonzero(-data_end >= self._drop_level)[0]
        data_end_wave_idxs = np.insert(data_end_wave_idxs, 0, -1, axis=0)
        data_end_peaks_idxs = data_end_wave_idxs[np.nonzero(np.diff(data_end_wave_idxs) > 1)[0] + 1]

        leakages = []
        filtered_peaks = []
        for peak_start, peak_end in zip(data_start_peaks_idxs.tolist(), data_end_peaks_idxs.tolist()):
            peaks_diff_t = abs(peak_end - peak_start) * self._pipeline.time_resolution
            if peaks_diff_t > 2*segment.flow_time:
                continue
            # TODO: experiment with resolutions
            diff_t_from_edge = (segment.flow_time - peaks_diff_t) / 2 if (segment.flow_time - peaks_diff_t) / 2 > 0 else 0
            diff_dist_from_edge = (diff_t_from_edge / 1000) * self._wave_speed
            leakage_position = segment.length - diff_dist_from_edge if peak_start > peak_end else diff_dist_from_edge
            leakage_time = (peak_start * self._pipeline.time_resolution) - segment.flow_time * (leakage_position / segment.length)
            leakage_position_idx = int(leakage_position / self._pipeline.length_resolution)
            leakage_time_idx = int(leakage_time / self._pipeline.time_resolution)
            filtered_peaks.append((peak_start, peak_end))
            leakages.append((leakage_position_idx, leakage_time_idx))

        time = np.arange(begin, end, self._pipeline.time_resolution) - window_begin
        position = np.arange(0, segment.length, self._pipeline.length_resolution)
        positions, _ = np.meshgrid(position, time)

        probability = self.simulate_probability(positions, filtered_peaks, segment.length)
        self.displayer.set_params(data_start, data_end, None, self, segment, begin, end, probability,
                                  [self._wave_speed, segment.length,
                                   self.pipeline.length_resolution, self.pipeline.time_resolution])
        return np.array(leakages)

    def find_leaks_in_range(self, begin: int, end: int) -> list[Event]:
        events = []
        self.displayer = DetectorDisplay()
        for segment in self._segments:
            alarm_start_time = self._pipeline.plant.get_leakage_alarm_delta() // self._pipeline.time_resolution
            if segment.no_detection_time - begin > alarm_start_time:
                alarm_start_time = int((segment.no_detection_time - begin) // self._pipeline.time_resolution)
            leakages = self.get_probability(segment, begin, end)
            if len(leakages) > 0:
                while alarm_start_time < int((end-begin) // self._pipeline.time_resolution):
                    leakage_idxs = np.where(leakages[:,1] >= alarm_start_time)[0]
                    if len(leakage_idxs) == 0:
                        break
                    leakage_position, leakage_time = leakages[leakage_idxs[0]]
                    events.append(Event(self._id, begin + leakage_time*self._pipeline.time_resolution, segment.begin_pos - self._pipeline.begin_pos + leakage_position * self._pipeline.length_resolution))
                    segment.no_detection_time = begin + leakage_time * self._pipeline.time_resolution + self._no_detection_window
                    alarm_start_time = int(self._no_detection_window // self._pipeline.time_resolution + leakage_time)

        events = self.choose_events(events, begin)

        for segment_number in range(len(self._segments)):
            self.displayer.display(segment_number, False, 1)

        return events

    def choose_events(self, events: list,  begin: int):
        for event in sorted(events, key=lambda ev: ev.time):
            if len(self._stored_events) == 0 or event.time - self._stored_events[-1].time > self._pipeline_flow_time:
                self._stored_events.append(event)
        self._stored_events = [event for event in self._stored_events if begin - event.time < self._pipeline_flow_time]
        return [event for event in self._stored_events if event.time >= begin]

    def find_leaks_to(self, end: int) -> list[Event]:
        pass
