import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta
from math import floor


class Plot(object):
    def __init__(self) -> None:
        pass

    def trend_graph(self, data, begin, end, timestep) -> None:
        dates = np.arange(begin, end, timestep)
        dates = [datetime.fromtimestamp(date / 1000.0) for date in dates]
        formatter = mdates.DateFormatter("%H:%M:%S")
        plt.gca().xaxis.set_major_formatter(formatter)
        plt.plot(dates, data)
        plt.xticks(rotation=75)
        plt.xlabel("Czas [ms]")
        plt.ylabel("Ciśnienie [MPa]")
        
    def probability_heatmap(self, data, begin, end, length) -> None:
        _, ax = plt.subplots()
        dates = list(map(datetime.fromtimestamp, [begin / 1000, end / 1000]))
        dates = mdates.date2num(dates)
        ax.imshow(data, extent=[dates[0], dates[1], length, 0], aspect='auto')
        ax.tick_params(length = 0, rotation=75)
        ax.xaxis_date()
        ax.set_xlabel("Czas [ms]")
        ax.set_ylabel("Odległość [m]")

    def show(self) -> None:
        plt.show()


global_plot = Plot()