import threading
import time
import scipy.signal

class Trend:

    def get_ID(self):
        return self.trend_ID

    def __init__(self, server,  trend_ID, window_size = 0):
        self.run_next_tick = int(time.time()) + 1
        self.trend_ID = int(trend_ID)
        self.data = 100*[None]
        self.window_size = window_size 
        self.server = server
        self.timestamp = None
        self.terminate = False

    def run(self):
        pass


class TrendQuick(Trend):
    

    def __init__(self, server, trend_ID, host_name, port,
                 slave_ID, register, raw_min,
                 raw_max, scaled_min, scaled_max ):
        super().__init__(server, trend_ID)
        self.send_next_tick = self.run_next_tick
        self.host_name = host_name
        self.port = int(port)
        self.slave_ID = int(slave_ID)
        self.register = int(register)
        self.raw_min = int(raw_min)
        self.raw_max = int(raw_max)
        self.scaled_min = int(scaled_min)
        self.scaled_max = int(scaled_max)

    def write(self, slave_id, function_code, address, value):
        self.timestamp = int(time.time())
        self.data[99 - address + self.register] = value

    def run(self):
        @self.server.route(slave_ids = [1], function_codes = [6, 16], addresses = list(range(self.register, self.register + 100)))
        def write(slave_id, function_code, address, value):
            self.timestamp = int(time.time())
            self.data[99 - address + self.register] = value


class TrendDeriv(Trend):
    
    def __init__(self, server, trend_ID,  trend_quick, window_size):
        super().__init__(server, trend_ID, int(window_size))
        self.send_next_tick = self.run_next_tick + 0.5  
        self.trend_quick = trend_quick
        self.queue = list()
        

    def run(self):
        self.timestamp = self.trend_quick.timestamp
        N = self.window_size
        cur_data = self.trend_quick.data

        if self.terminate:
            return

        if self.timestamp and not None in cur_data :
            if self.run_next_tick - self.timestamp != 1:
                cur_data = 100 * [ cur_data[0] ]
            self.queue = self.queue + cur_data

        if len(self.queue) == 2 * N + 100 :
            kernel = list(range(-N, N + 1))
            norm = 1/(N * (N + 1))
            self.data = list(map(int, scipy.signal.fftconvolve(self.queue, kernel, mode='valid') *norm))
            self.queue = self.queue[100:]

        
        self.run_next_tick = self.run_next_tick + 1
        threading.Timer(self.run_next_tick - time.time(), self.run).start()

    

class TrendMean(Trend):

    def __init__(self, server, trend_ID,  trend_quick, window_size):
        super().__init__(server, trend_ID, int(window_size))
        self.send_next_tick = self.run_next_tick + 0.5
        self.trend_quick = trend_quick
        self.queue = list()
        

    def run(self):
        self.timestamp = self.trend_quick.timestamp
        N = self.window_size
        cur_data = self.trend_quick.data

        if self.terminate:
            return

        if self.timestamp and not None in cur_data :
            if self.run_next_tick - self.timestamp != 1:
                cur_data = 100 * [ cur_data[0] ]
            self.queue = self.queue + cur_data

        if len(self.queue) == 2 * N + 100 :
            kernel = (2 * N + 1) * [0]
            norm = 1/(N*(N+1))
            self.data = list(map(int, scipy.signal.fftconvolve(self.queue, kernel, mode='valid') * norm))
            self.queue = self.queue[100:]

        self.run_next_tick = self.run_next_tick + 1
        threading.Timer(self.run_next_tick - time.time(), self.run).start()

