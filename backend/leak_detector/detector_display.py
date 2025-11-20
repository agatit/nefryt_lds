import datetime
import logging
from typing import Any
import matplotlib.backend_bases
import seaborn as sns
import numpy as np
from matplotlib import pyplot as plt, patheffects
from leak_detector.method import MethodBase
from leak_detector.segment import Segment


def detector_display(method: MethodBase, plot: bool, segment: Segment, begin: int, end: int, probability: np.ndarray,
             data_start: np.ndarray, data_end: np.ndarray, dp_indexes_list: list,
             past_data_start: np.ndarray | None = None, past_data_end: np.ndarray | None = None) -> None:
    step_xtick_ms = 1000
    step_ytick_m = 50

    xticks_labels = [str(datetime.datetime.fromtimestamp(t // 1000).strftime('%H:%M:%S'))
                     for t in
                     np.arange(begin - segment.max_window_size, end + segment.max_window_size + 1, 10).tolist()]
    yticks_labels = np.arange(segment.begin_pos, segment.begin_pos + segment.length,
                              method.pipeline.length_resolution).astype(int)

    step = 200
    for part in range(probability.shape[0] // step):
        proba_now = probability[part * step:(part + 1) * step, :]
        max_x, max_y = np.unravel_index(np.argmax(proba_now), proba_now.shape)
        logging.info(f'Method ID={method.id}: '
                     f'Segment [{segment.start.id}-{segment.end.id}]: '
                     f'Max({float(yticks_labels[max_y])}, '
                     f'{xticks_labels[part * step + segment.max_window_size // 10 + int(max_x)]}.{((part * step + int(max_y)) % 100) * 10:03d}) '
                     f'= {proba_now[max_x, max_y]}')
    if plot:
        fig, ax = plt.subplots(figsize=(16, 8), constrained_layout=True)
        ax.set_frame_on(False)
        ax.set_xticks([])
        ax.set_yticks([])

        ax1 = fig.add_axes((0.02, 0.75, 0.96, 0.25))
        heatmap_width = (end - begin) / (2 * segment.max_window_size + end - begin) * 0.92
        heatmap_x0 = 0.5 - heatmap_width / 2
        heatmap_y0 = 0.06
        heatmap_height = 0.6
        ax2 = fig.add_axes((heatmap_x0, heatmap_y0, heatmap_width, heatmap_height))
        ax_cbar = fig.add_axes((0.5 + heatmap_width / 2 + 0.05, 0.06, 0.02, 0.6))

        ax1.plot(np.arange(0, (2 * segment.max_window_size + end - begin) // 10),
                 data_start,
                 label=f'Start PT (TrendID={segment.start.id}) data')
        ax1.plot(np.arange(0, (2 * segment.max_window_size + end - begin) // 10),
                 data_end,
                 label=f'End PT (TrendID={segment.end.id}) data')
        if past_data_start is not None:
            ax1.plot(np.arange(0, (2 * segment.max_window_size + end - begin) // 10),
                     past_data_start,
                     label=f'Past start PT (TrendID={segment.start.id}) data')
        if past_data_end is not None:
            ax1.plot(np.arange(0, (2 * segment.max_window_size + end - begin) // 10),
                     past_data_end,
                     label=f'End start PT (TrendID={segment.end.id}) data')
        ax1.set_xticks((np.arange(0, (2 * segment.max_window_size + end - begin) // 10 + 1))[::step_xtick_ms // 10])
        ax1.set_xticklabels(xticks_labels[::step_xtick_ms // 10], rotation=45, ha='right')
        ax1.margins(x=0.02)
        ax1.legend()

        ax2 = sns.heatmap(probability.T, ax=ax2, cbar_ax=ax_cbar, vmin=0, vmax=np.max(probability))
        ax2.set_xticks((np.arange(0, (end - begin) // method.pipeline.time_resolution + 1))[
                       ::step_xtick_ms // method.pipeline.time_resolution])
        ax2.set_xticklabels(
            xticks_labels[segment.max_window_size // 10:-segment.max_window_size // 10:step_xtick_ms // 10],
            rotation=45, ha='right')

        ax2.set_yticks(np.arange(0, segment.length // method.pipeline.length_resolution, 1)[
                       ::step_ytick_m // method.pipeline.length_resolution])
        ax2.set_yticklabels(yticks_labels[::step_ytick_m // method.pipeline.length_resolution])
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
                label_x = x - 8 if x > probability.shape[1] // 2 else x + 8
                ha = 'right' if x > probability.shape[1] // 2 else 'left'
                dp1_value = round(float(data_start[dp_indexes_list[0][x,y]]), 2)
                dp2_value = round(float(data_end[dp_indexes_list[1][x,y]]), 2)
                dp3_value = round(float(data_start[dp_indexes_list[2][x,y]]), 2)
                dp4_value = round(float(data_end[dp_indexes_list[3][x,y]]), 2)
                proba_start = round((dp1_value - dp4_value), 2) if (dp1_value - dp4_value) > 0 else 0
                proba_end = round((dp2_value - dp3_value), 2) if (dp2_value - dp3_value) > 0 else 0
                label = ax2.text(label_x, y + 8,
                                 f"P({yticks_labels[y]}m, "
                                 f"{xticks_labels[segment.max_window_size // 10:-segment.max_window_size // 10][x]}.{(x * 10) % 1000:03d})"
                                 f" = {proba_start} * {proba_end} = {probability[x, y]}",
                                 color='white', fontsize=12, ha=ha, va='bottom')
                label.set_path_effects([patheffects.withStroke(linewidth=2, foreground='black')])
                heatmap_objects.extend([point, label])

                colors = ['green', 'gold', 'purple', 'silver']
                x_positions = [dp_indexes[x, y] for dp_indexes in dp_indexes_list]
                for i, (x_pos, color) in enumerate(zip(x_positions, colors)):
                    y_pos = data_start[x_pos] if i % 2 == 0 else data_end[x_pos]
                    line = ax1.axvline(x=x_pos, color=color, lw=1.5, label=f'dp{i + 1}({x_pos}, {round(y_pos, 2)})')
                    point = ax1.plot(x_pos, y_pos, 'o', color=color)[0]
                    plot_objects.extend([line, point])
                handles, labels = ax1.get_legend_handles_labels()
                ax1.legend(handles, labels)

                fig.canvas.draw_idle()

        fig.canvas.mpl_connect("button_press_event", on_click)  # noqa
        plt.show()
        