import datetime
import logging
from typing import Any
import matplotlib.backend_bases
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.interpolate import interp1d
from .base import MethodBase, Segment
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
                    end_time = (segment.current_detection_end_time - begin) // self._pipeline.time_resolution \
                        if segment.current_detection_end_time < end else -1
                    max_position, max_time = np.unravel_index(np.argmax(probability[:, :end_time]), probability[:, :end_time].shape)
                    max_probability = probability[max_position, int(max_time)]
                    leakage = Leakage(float(max_probability), int(max_position), begin+int(max_time)*self._pipeline.time_resolution)
                    if leakage.probability > segment.current_leakage.probability:
                        segment.current_leakage = leakage
                    if segment.current_detection_end_time < end:
                        leakage_position = segment.begin_pos + segment.current_leakage.position * self._pipeline.length_resolution
                        leakage_time = (
                            f'{datetime.datetime.fromtimestamp(segment.current_leakage.timestamp//1000)}'
                            f'.{leakage.timestamp%1000}')
                        leakage_probability = segment.current_leakage.probability
                        segment.current_leakage = None
                        segment.current_detection_end_time = None
                        print(f'ALARM: Leakage detected in position = {leakage_position} and time = {leakage_time} with probability = {leakage_probability}')

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
                print(first_time, end_time)
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
                leakage_position = leakage_segment.begin_pos + leakage.position * self._pipeline.length_resolution
                leakage_time = (f'{datetime.datetime.fromtimestamp(leakage.timestamp//1000)}'
                                f'.{leakage.timestamp%1000}')
                leakage_probability = leakage.probability
                print(f'ALARM: Leakage detected in position = {leakage_position} and time = {leakage_time} with probability = {leakage_probability}')

            for segment in self._segments:
                segment.no_detection_time = begin + first_leakage_time*self._pipeline.time_resolution + self._no_detection_window

        return events

    def _display(self, plot: bool, segment: Segment, begin: int, end: int, probability: np.ndarray,
                 data_start: np.ndarray, data_end: np.ndarray, dp_indexes_list: list, past_data_start: np.ndarray | None = None,
                 past_data_end: np.ndarray | None = None) -> None:
        step_xtick_ms = 1000
        step_ytick_m = 50

        xticks_labels = [str(datetime.datetime.fromtimestamp(t // 1000).strftime('%H:%M:%S'))
                         for t in np.arange(begin-segment.max_window_size, end+segment.max_window_size+1, 10).tolist()]
        yticks_labels = np.arange(segment.begin_pos, segment.begin_pos + segment.length, self._pipeline.length_resolution).astype(int)

        max_x, max_y = np.unravel_index(np.argmax(probability), probability.shape)
        print(f'Method ID={self._id}: '
              f'Segment [{segment.start.id}-{segment.end.id}]: '
              f'Max({float(yticks_labels[max_x])}, '
              f'{xticks_labels[segment.max_window_size//10 + int(max_y)]}.{(int(max_y)%100)*10:03d}) '
              f'= {probability[max_x, max_y]}')

        if plot:
            fig, ax = plt.subplots(figsize=(16,8), constrained_layout=True)
            ax.set_frame_on(False)
            ax.set_xticks([])
            ax.set_yticks([])

            ax1 = fig.add_axes((0.02, 0.75, 0.96, 0.25))
            heatmap_width = (end-begin) / (2*segment.max_window_size + end - begin) * 0.92
            heatmap_x0 = 0.5 - heatmap_width/2
            heatmap_y0 = 0.06
            heatmap_height = 0.6
            ax2 = fig.add_axes((heatmap_x0, heatmap_y0, heatmap_width, heatmap_height))
            ax_cbar = fig.add_axes((0.5 + heatmap_width/2 + 0.05, 0.06, 0.02, 0.6))

            ax1.plot(np.arange(0, (2*segment.max_window_size+end-begin)//10),
                       data_start,
                       label=f'Start PT (TrendID={segment.start.id}) data')
            ax1.plot(np.arange(0, (2*segment.max_window_size+end-begin)//10),
                       data_end,
                       label=f'End PT (TrendID={segment.end.id}) data')
            if past_data_start is not None:
                ax1.plot(np.arange(0, (2*segment.max_window_size+end-begin)//10),
                         past_data_start,
                         label=f'Past start PT (TrendID={segment.start.id}) data')
            if past_data_end is not None:
                ax1.plot(np.arange(0, (2 * segment.max_window_size + end - begin) // 10),
                         past_data_end,
                         label=f'End start PT (TrendID={segment.end.id}) data')
            ax1.set_xticks((np.arange(0, (2*segment.max_window_size+end-begin)//10+1))[::step_xtick_ms//10])
            ax1.set_xticklabels(xticks_labels[::step_xtick_ms//10], rotation=45, ha='right')
            ax1.margins(x=0.02)
            ax1.legend()

            ax2 = sns.heatmap(probability, ax=ax2, cbar_ax=ax_cbar, vmin=0, vmax=5*1e-2)
            ax2.set_xticks((np.arange(0, (end-begin)//self._pipeline.time_resolution+1))[::step_xtick_ms//self._pipeline.time_resolution])
            ax2.set_xticklabels(xticks_labels[segment.max_window_size//10:-segment.max_window_size//10:step_xtick_ms//10], rotation=45, ha='right')

            ax2.set_yticks(np.arange(0, segment.length // self._pipeline.length_resolution, 1)[::step_ytick_m//self._pipeline.length_resolution])
            ax2.set_yticklabels(yticks_labels[::step_ytick_m//self._pipeline.length_resolution])
            ax2.set(xlabel="Time [s]", ylabel="Distance [m]")

            heatmap_objects = []
            plot_objects = []

            def on_click(event: matplotlib.backend_bases.MouseEvent) -> Any:
                nonlocal heatmap_objects, plot_objects
                if event is not None and event.inaxes == ax2:
                    for obj in heatmap_objects:
                        obj.remove()
                    for obj in plot_objects:
                        obj.remove()
                    heatmap_objects.clear()
                    plot_objects.clear()

                    x, y = event.xdata, event.ydata
                    x = int(x)
                    y = int(y)
                    point = ax2.plot(x, y, 'ro', markersize=8)[0]
                    label = ax2.text(x + 8, y + 8,
                                     f"P({yticks_labels[y]}m, "
                                     f"{xticks_labels[segment.max_window_size//10:-segment.max_window_size//10][x]}.{(x*10)%1000:03d})"
                                     f"={probability[y, x]}",
                        color='white', fontsize=12)
                    heatmap_objects.extend([point, label])

                    colors = ['green', 'gold', 'purple', 'silver']
                    x_positions = [dp_indexes[y][x] for dp_indexes in dp_indexes_list]
                    for i, (x_pos, color) in enumerate(zip(x_positions, colors)):
                        line = ax1.axvline(x=x_pos, color=color, lw=1.5, label=f'dp{i+1}')
                        y_pos = data_start[x_pos] if i%2==0 else data_end[x_pos]
                        point = ax1.plot(x_pos, y_pos, 'o', color=color)[0]
                        plot_objects.extend([line, point])
                    handles, labels = ax1.get_legend_handles_labels()
                    ax1.legend(handles, labels)

                    fig.canvas.draw_idle()

            fig.canvas.mpl_connect("button_press_event", on_click) # noqa
            plt.show()

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

        dp1 = np.array(data_start)[dp1_indexes] / (self._normal_range * wave_fading_left)
        dp2 = np.array(data_end)[dp2_indexes] / (self._normal_range * wave_fading_right)
        dp3 = np.array(data_start)[dp3_indexes] / (self._normal_range * wave_fading_left)
        dp4 = np.array(data_end)[dp4_indexes] / (self._normal_range * wave_fading_right)

        probability = dp3 * dp4 - dp1 * dp2
        probability = np.sqrt(np.maximum(probability, 0))
        probability = np.minimum(probability, 1)
        self._display(True, segment, begin, end, probability, data_start, data_end,
                      [dp1_indexes, dp2_indexes, dp3_indexes, dp4_indexes])

        return probability

class MethodWaveUnsigned(MethodWave):
    def get_probability(self, segment: Segment, begin: int, end: int) -> np.ndarray:
        window_begin = begin - segment.max_window_size
        window_end = end + segment.max_window_size

        data_start1 = np.abs(segment.start.get_trend_data(window_begin, window_end))
        data_end1 = np.abs(segment.end.get_trend_data(window_begin, window_end))

        past_delay = int(1000*self._pipeline_length / self._wave_speed)
        past_window_begin = window_begin - past_delay
        past_window_end = window_end - past_delay

        past_data_start = segment.start.get_trend_data(past_window_begin, past_window_end, 10)
        past_data_end = segment.end.get_trend_data(past_window_begin, past_window_end, 10)
        interp_func_start = interp1d(np.arange(0, len(data_start1)+1, 10), past_data_start, kind='linear', bounds_error=False,
                                     fill_value=0)
        interp_func_end = interp1d(np.arange(0, len(data_end1)+1, 10), past_data_end, kind='linear', bounds_error=False, fill_value=0)

        past_data_start = np.abs(interp_func_start(np.arange(len(data_start1))))
        past_data_end = np.abs(interp_func_end(np.arange(len(data_end1))))
        past_data_wave_fading = np.exp(self._wave_coeff * self._pipeline_length)
        data_start2 = data_start1 - past_data_start / past_data_wave_fading
        data_end2 = data_end1 - past_data_end / past_data_wave_fading

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

        dp1 = np.abs(np.array(data_start2))[dp1_indexes] / (self._normal_range * wave_fading_left)
        dp2 = np.abs(np.array(data_end2))[dp2_indexes] / (self._normal_range * wave_fading_right)
        dp3 = np.abs(np.array(data_start2))[dp3_indexes] / (self._normal_range * wave_fading_left)
        dp4 = np.abs(np.array(data_end2))[dp4_indexes] / (self._normal_range * wave_fading_right)

        probability = dp3 * dp4 - dp1 * dp2
        probability = np.sqrt(np.maximum(probability, 0))
        probability = np.minimum(probability, 1)
        self._display(False, segment, begin, end, probability, data_start1, data_end1,
                      [dp1_indexes, dp2_indexes, dp3_indexes, dp4_indexes])
                      # past_data_start / past_data_wave_fading, past_data_end / past_data_wave_fading)

        return probability
