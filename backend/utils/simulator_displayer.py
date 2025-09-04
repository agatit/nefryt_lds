import os
import sys
from multiprocessing.connection import Client
import matplotlib.pyplot as plt
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simulator.config import SimulatorSettings

SIMULATION_ID = 1

def display_simulation_data():
    if SimulatorSettings.displayer_port:
        conn = Client(('localhost', SIMULATION_ID+SimulatorSettings.displayer_port), authkey=b'secret')
        try:
            plt.ion()
            fig, ax = plt.subplots()
            line, = ax.plot([], [], '-')

            while True:
                length, values = conn.recv()
                dists = np.linspace(0, length, len(values))
                line.set_xdata(dists)
                line.set_ydata(values)
                plt.xlim(0, max(dists))
                plt.ylim(0, max(values)+1)
                plt.draw()
                plt.pause(0.1)
        except (KeyboardInterrupt, ConnectionResetError):
            conn.close()
    else:
        print('No port set in Simulator module settings')

if __name__ == "__main__":
    display_simulation_data()
