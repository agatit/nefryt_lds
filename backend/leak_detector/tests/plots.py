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
        
    def probability_heatmap(self, data, time, position) -> None:
        dates = list(map(datetime.fromtimestamp, [time[0] / 1000, time[-1] / 1000]))
        dates = mdates.date2num(dates)
        fig, ax = plt.subplots()
        im = ax.pcolormesh(time, position, data)
        ax.set_xlabel("Pozycja na rurociągu")
        ax.set_ylabel("czas")
        cb = fig.colorbar(im, ax=ax)
        cb.set_label(label='Wartość wskaźnika')

    def scatter_points(self, x, y):
        _, ax = plt.subplots()
        ax.scatter(x, y)

    def show(self) -> None:
        plt.show()


global_plot = Plot()