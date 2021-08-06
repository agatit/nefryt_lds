from datetime import datetime
from sys import maxsize
import threading
import time
import threading
import scipy
from scipy import signal

begin_time = time.time()

def get_time_delay():
    return int(time.time()) + 1 - time.time()

class Trend:

    def get_ID(self):
        return self.trend_ID

    def __init__(self, server,  trend_ID):
        self.trend_ID = int(trend_ID)
        self.data = 100*[0]
        self.timestamp = time.time()
        self.window_size = 0
        self.server = server
        pass

    def run(self):
        pass


class TrendQuick(Trend):
    # powinien uruchamiać wątki serwera modbus
    def __init__(self, server, trend_ID, host_name, port,
                 slave_ID, register, raw_min,
                 raw_max, scaled_min, scaled_max ):
        super().__init__(server, trend_ID)
        self.host_name = host_name
        self.port = int(port)
        self.slave_ID = int(slave_ID)
        self.register = int(register)
        self.raw_min = int(raw_min)
        self.raw_max = int(raw_max)
        self.scaled_min = int(scaled_min)
        self.scaled_max = int(scaled_max)
        self.data = 100*[0]

    def read(self, slave_id, function_code, address):
        return self.data[address - self.register]

    def write(self, slave_id, function_code, address, value):
        self.timestamp = time.time()
        self.data[address - self.register] = value

    def run(self):
        self.server.route_map.add_rule(self.read, [1], [3, 4], list(range(self.register, self.register + 100)))
        self.server.route_map.add_rule(self.write, [1], [6, 16], list(range(self.register, self.register + 100)))


class TrendDeriv(Trend):
    
    def __init__(self, server, trend_ID,  trend_quick, window_size):
        super().__init__(server, trend_ID)
        self.trend_quick = trend_quick
        self.data = 100*[0]
        self.window_size = int(window_size)
        self.queue = list()
        

    def run(self):
        threading.Timer( get_time_delay(), self.run).start()
        self.timestamp = time.time()
        N = self.window_size
        cur_data = self.trend_quick.data

        if len(self.queue) == 2 * N + 100 :
            kernel = list(range(-N, N + 1))
            self.data = list(map(int, scipy.signal.fftconvolve(self.queue, kernel, mode='valid') * (1/(N*(N+1)))))
            self.queue = self.queue[100:]

        if int(begin_time) != int(self.trend_quick.timestamp) :
            self.queue = self.queue + cur_data
    

class TrendMean(Trend):

    def __init__(self, server, trend_ID,  trend_quick, window_size):
        super().__init__(server, trend_ID)
        self.trend_quick = trend_quick
        self.data = 100*[0]
        self.window_size = int(window_size)
        self.queue = list()
        

    def run(self):
        threading.Timer(get_time_delay(), self.run).start()
        N = self.window_size
        cur_data = self.trend_quick.data

        if len(self.queue) == 2 * N + 100 :
            self.timestamp = time.time()

            for i in range(100) : 
                index = i
                suma = self.queue[i]
                while index < 2*N :
                    index = index + 100
                    suma = suma + self.queue[index]
                self.data[i] =  suma // (N//50 + 1)

            self.queue = self.queue[100:]

        if int(begin_time) != int(self.trend_quick.timestamp) :
            self.queue = self.queue + cur_data
