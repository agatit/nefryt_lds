import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime


class Plot:
    @staticmethod
    def trend_graph(data, begin, end, timestep) -> None:
        dates = np.arange(begin, end, timestep)
        dates = [datetime.fromtimestamp(date / 1000.0) for date in dates]
        formatter = mdates.DateFormatter("%H:%M:%S")
        plt.gca().xaxis.set_major_formatter(formatter)
        plt.plot(dates, data)
        plt.xticks(rotation=75)
        plt.xlabel("Time [ms]")
        plt.ylabel("Pressure [MPa]")

    @staticmethod
    def probability_heatmap(data, time, position) -> None:
        dates = list(map(datetime.fromtimestamp, time / 1000))
        fig, ax = plt.subplots()
        im = ax.pcolormesh(dates, position, data)
        ax.set_ylabel("Position")
        ax.set_xlabel("Time")
        cb = fig.colorbar(im, ax=ax)
        cb.set_label(label='Probability value')

    @staticmethod
    def scatter_points(x, y) -> None:
        _, ax = plt.subplots()
        ax.scatter(x, y)

    @staticmethod
    def show() -> None:
        plt.show()
