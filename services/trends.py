import time

#KAROL: każda klasa ma przynajmniej jeden argument i jest to Trend_ID
class Trend:

    def get_ID(self):
        return self.trend_ID

    def __init__(self, server,  trend_ID):
        self.trend_ID = int(trend_ID)
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
        self.timestamp = time.time()

    def read(self, slave_id, function_code, address):
        return self.data[address - self.register]

    def write(self, slave_id, function_code, address, value):
        self.timestamp = time.time()
        self.data[address - self.register] = value

    def run(self):
        self.server.route_map.add_rule(self.read, [1], [3, 4], list(range(self.register, self.register + 100)))
        self.server.route_map.add_rule(self.write, [1], [6, 16], list(range(self.register, self.register + 100)))
        pass

    def __str__(self):
        return  str(self.trend_ID) + ', ' + str(self.host_name) + ', ' +  str(self.port) + ', ' + str(self.slave_ID) + '...'    


class TrendDeriv(Trend):
    # powinien uruchamiać wątek przeliczający, parametrem konstruktora powinien być TrendQuick
    # powinien utrzymywać bufor wartości i uzupełniać ją wartościami z quick trendu
    def __init__(self, server, trend_ID,  trend_quick, window_size):
        super().__init__(server, trend_ID)
        self.trend_quick = trend_quick
        self.window_size = window_size

    def __str__(self):
        return str(self.trend_ID) + ", " +  str(self.trend_quick) + ", " + str(self.window_size)

class TrendMean(Trend):
    # j.w.
    def __init__(self, server, trend_ID, trend_quick, window_size):
        super().__init__(server, trend_ID)
        self.trend_quick = trend_quick
        self.window_size = window_size
        pass

    def __str__(self):
        return str(self.trend_ID) + ", " +  str(self.trend_quick) + ", " + str(self.window_size)