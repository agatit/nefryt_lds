import os
import sys
import threading
from multiprocessing.connection import Client
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from simulator.config import SimulatorSettings

simulation_datas = {}
stop_flag = threading.Event()


def receive_data(simulation_id):
    conn = Client(('localhost', SimulatorSettings.displayer_ports[simulation_id]), authkey=b'secret')
    try:
        while not stop_flag.is_set():
            length, values = conn.recv()
            dists = np.linspace(0, length, len(values))
            simulation_datas[simulation_id]['sim_data'] = (dists, values)
    except ConnectionResetError:
        pass
    finally:
        conn.close()


def display_simulation_data():
    if SimulatorSettings.displayer_ports:
        colors = list(mcolors.BASE_COLORS.values())
        plt.ion()
        fig, ax = plt.subplots()

        for i, simulation_id in enumerate(SimulatorSettings.displayer_ports.keys()):
            line, = ax.plot([], [], '-', color=colors[i % len(colors)],
                            label=f'Simulation id={simulation_id}')
            simulation_datas[simulation_id] = {
                'line': line, 
                'sim_data': None
            }
            threading.Thread(target=receive_data, args=(simulation_id,), daemon=True).start()
        try:
            while True:
                for simulation_id, value in simulation_datas.items():
                    line, sim_data = value['line'], value['sim_data']
                    if sim_data is not None:
                        dists, values = sim_data
                        line.set_xdata(dists)
                        line.set_ydata(values)
                    ax.relim()
                    ax.autoscale_view()
                    plt.legend(loc=2)
                    plt.draw()
                plt.pause(0.1)
        except (KeyboardInterrupt, ConnectionResetError):
            stop_flag.set()
    else:
        print('No port set in Simulator module settings')


if __name__ == '__main__':
    display_simulation_data()
