import datetime
import logging
from typing import Any
import matplotlib.backend_bases
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt, patheffects
from leak_detector.method import MethodBase
from leak_detector.segment import Segment


class DetectorDisplay:
    def __init__(self):
        self.dp_indexes_lists = []
        self.data_starts = []
        self.data_ends = []
        self.methods = []
        self.segments = []
        self.begins = []
        self.ends = []
        self.probabilities = []
        self.peak_data_lists = []
        self.past_data_starts = []
        self.past_data_ends = []

    def set_params(self, data_start: np.ndarray, data_end: np.ndarray, dp_indexes_list: list | None,
                   method: MethodBase, segment: Segment, begin: int, end: int, probability: np.ndarray,
                   peak_data_list: list | None, past_data_start: np.ndarray | None = None, past_data_end: np.ndarray | None = None) -> None:
        self.data_starts.append(data_start)
        self.data_ends.append(data_end)
        self.dp_indexes_lists.append(dp_indexes_list)
        self.methods.append(method)
        self.segments.append(segment)
        self.begins.append(begin)
        self.ends.append(end)
        self.probabilities.append(probability)
        self.peak_data_lists.append(peak_data_list)
        self.past_data_starts.append(past_data_start)
        self.past_data_ends.append(past_data_end)

    def display(self, segment_number: int, plot: bool, vmax: float, traces: list | None = None) -> None:
        step_xtick_ms = 1000
        step_ytick_m = 50

        begin = self.begins[segment_number]
        end = self.ends[segment_number]
        segment = self.segments[segment_number]
        method = self.methods[segment_number]
        probability = self.probabilities[segment_number]
        dp_indexes_list = self.dp_indexes_lists[segment_number]
        data_start = self.data_starts[segment_number]
        data_end = self.data_ends[segment_number]
        peak_data_list = self.peak_data_lists[segment_number]
        past_data_start = self.past_data_starts[segment_number]
        past_data_end = self.past_data_ends[segment_number]

        xticks_labels = [str(datetime.datetime.fromtimestamp(t // 1000).strftime('%H:%M:%S'))
                         for t in
                         np.arange(begin - segment.max_window_size[0], end + segment.max_window_size[1] + 1, 10).tolist()]
        yticks_labels = np.arange(segment.begin_pos, segment.begin_pos + segment.length,
                                  method.pipeline.length_resolution).astype(int)

        max_x, max_y = np.unravel_index(np.argmax(probability), probability.shape)
        logging.info(f'Method ID={method.id}: '
                     f'Segment [{segment.start.id}-{segment.end.id}]: '
                     f'Max({float(yticks_labels[max_y])}, '
                     f'{xticks_labels[segment.max_window_size[0] // 10 + int(max_x)]}.{((int(max_y)) % 100) * 10:03d}) '
                     f'= {probability[max_x, max_y]}')
        if plot:
            fig, ax = plt.subplots(figsize=(16, 8), constrained_layout=True)
            ax.set_frame_on(False)
            ax.set_xticks([])
            ax.set_yticks([])

            ax1 = fig.add_axes((0.03, 0.75, 0.94, 0.25))
            heatmap_width = (end - begin) / (sum(segment.max_window_size) + end - begin) * 0.9
            heatmap_x0 = (0.5 - heatmap_width / 2 - (heatmap_width / (sum(segment.max_window_size) + end - begin))
                          * (segment.max_window_size[1] - segment.max_window_size[0]) / 2)
            heatmap_y0 = 0.06
            heatmap_height = 0.6
            ax2 = fig.add_axes((heatmap_x0, heatmap_y0, heatmap_width, heatmap_height))
            ax2.set_xmargin(0)
            ax_cbar = fig.add_axes((0.5 + heatmap_width / 2 + 0.05, 0.06, 0.02, 0.6))

            ax1.plot(np.arange(0, (sum(segment.max_window_size) + end - begin) // 10),
                     data_start, label=f'Start PT (TrendID={segment.start.id}) data')
            ax1.plot(np.arange(0, (sum(segment.max_window_size) + end - begin) // 10),
                     data_end, label=f'End PT (TrendID={segment.end.id}) data')
            if past_data_start is not None:
                ax1.plot(np.arange(0, (sum(segment.max_window_size) + end - begin) // 10),
                         past_data_start, label=f'Past start PT (TrendID={segment.start.id}) data')
            if past_data_end is not None:
                ax1.plot(np.arange(0, (sum(segment.max_window_size) + end - begin) // 10),
                         past_data_end, label=f'End start PT (TrendID={segment.end.id}) data')
            ax1.set_xticks((np.arange(0, (sum(segment.max_window_size) + end - begin) // 10 + 1))[::step_xtick_ms // 10])
            ax1.set_xticklabels(xticks_labels[::step_xtick_ms // 10], rotation=45, ha='right')
            ax1.margins(x=0.02)
            ax1.legend()

            ax2 = sns.heatmap(probability.T, ax=ax2, cbar_ax=ax_cbar, vmin=0, vmax=vmax)
            ax2.set_xticks((np.arange(0, (end - begin) // method.pipeline.time_resolution + 1))[
                           ::step_xtick_ms // method.pipeline.time_resolution])
            ax2.set_xticklabels(
                xticks_labels[segment.max_window_size[0] // 10:-segment.max_window_size[1] // 10:step_xtick_ms // 10],
                rotation=45, ha='right')

            ax2.set_yticks(np.arange(0, segment.length // method.pipeline.length_resolution, 1)[
                           ::step_ytick_m // method.pipeline.length_resolution])
            ax2.set_yticklabels(yticks_labels[::step_ytick_m // method.pipeline.length_resolution])
            ax2.set(xlabel="Time [s]", ylabel="Distance [m]")
            if traces:
                for trace in traces:
                    trace = np.array(trace)
                    trace_times = trace[:, 0]
                    trace_positions = trace[:, 1]
                    ax2.scatter(trace_times[-1], trace_positions[-1], marker='X', color='white', s=200)
                    ax2.scatter(trace_times[0], trace_positions[0], marker='o', color='white', s=100)
                    ax2.plot(trace_times, trace_positions, color='white')

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
                    label_x = x - 8 if x > probability.shape[0] // 2 else x + 8
                    ha = 'right' if x > probability.shape[0] // 2 else 'left'
                    if dp_indexes_list:
                        dp1_value = round(float(data_start[dp_indexes_list[0][x,y]]), 2)
                        dp2_value = round(float(data_end[dp_indexes_list[1][x,y]]), 2)
                        dp3_value = round(float(data_start[dp_indexes_list[2][x,y]]), 2)
                        dp4_value = round(float(data_end[dp_indexes_list[3][x,y]]), 2)
                        proba_start = round((dp1_value - dp4_value), 2) if (dp1_value - dp4_value) > 0 else 0
                        proba_end = round((dp2_value - dp3_value), 2) if (dp2_value - dp3_value) > 0 else 0
                        label = ax2.text(label_x, y + 8,
                                         f"P({yticks_labels[y]}m, "
                                         f"{xticks_labels[segment.max_window_size[0] // 10:-segment.max_window_size[1] // 10][x]}.{(x * 10) % 1000:03d})"
                                         f" = {proba_start} * {proba_end} = {probability[x, y]}",
                                         color='white', fontsize=12, ha=ha, va='bottom')
                    else:
                        label = ax2.text(label_x, y + 8,
                                         f"P({yticks_labels[y]}m, "
                                         f"{xticks_labels[segment.max_window_size[0] // 10:-segment.max_window_size[1] // 10][x]}.{(x * 10) % 1000:03d})"
                                         f" = {probability[x, y]}",
                                         color='white', fontsize=12, ha=ha, va='bottom')
                    label.set_path_effects([patheffects.withStroke(linewidth=2, foreground='black')])
                    heatmap_objects.extend([point, label])

                    if dp_indexes_list:
                        colors = ['green', 'gold', 'purple', 'silver']
                        x_positions = [dp_indexes[x, y] for dp_indexes in dp_indexes_list]
                        for i, (x_pos, color) in enumerate(zip(x_positions, colors)):
                            y_pos = data_start[x_pos] if i % 2 == 0 else data_end[x_pos]
                            line = ax1.axvline(x=x_pos, color=color, lw=1.5,
                                               label=f'dp{i + 1}({x_pos}, {round(y_pos, 2)})')
                            point = ax1.plot(x_pos, y_pos, 'o', color=color)[0]
                            plot_objects.extend([line, point])
                        handles, labels = ax1.get_legend_handles_labels()
                        ax1.legend(handles, labels)
                    if peak_data_list:
                        colors = ['green', 'gold']
                        (wave_speed, segment_length, length_resolution, time_resolution) = peak_data_list
                        y *= length_resolution
                        delta_x_start = int((y / wave_speed) *(1000/time_resolution))
                        delta_x_end = int(((segment_length - y) / wave_speed) *(1000/time_resolution))
                        x_start = x + delta_x_start
                        x_end = x + delta_x_end
                        y_start = data_start[x_start]
                        y_end = data_end[x_end]
                        line_start = ax1.axvline(x=x_start, color=colors[0], lw=1.5, label=f'peak start={x_start}, {round(y_start, 1)}')
                        point_start = ax1.plot(x_start, y_start, 'o', color=colors[0])[0]
                        line_end = ax1.axvline(x=x_end, color=colors[1], lw=1.5, label=f'peak end={x_end}, {round(y_end, 1)}')
                        point_end = ax1.plot(x_end, y_end, 'o', color=colors[1])[0]
                        plot_objects.extend([line_start, point_start, line_end, point_end])
                        handles, labels = ax1.get_legend_handles_labels()
                        ax1.legend(handles, labels)

                    fig.canvas.draw_idle()

            fig.canvas.mpl_connect("button_press_event", on_click)  # noqa
            plt.show()
