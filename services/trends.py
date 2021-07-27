
class Trend:
    def __init__(self):
        pass

    def run(self):
        pass


class TrendQuick(Trend):
    # powinien uruchamiać wątki serwera modbus
    pass


class TrandDeriv(Trend):
    # powinien uruchamiać wątke przeliczajcy, parametrem konstrukora powinein być TrendQuick
    # powinien utrzymywać bufor wartości i uzupełniać ją wartościami z quick trendu
    def __init__(self, trend_quick, window_size):
        pass


class TrendMean(Trend):
    # j.w.
    def __init__(self, trend_quick, window_size):
        pass


class TrendWriter:
    def __init__(self, connection_string):
        # buduje listę obiektów odpowiednich klas na podstawie bazy danych
        # inicjalizuje je właściwymi parametrami
        self.trend_list = []

    def run(self):
        for t in self.trend_list:
            t.run()  # ..czy jakoś tak


if __name__ == "__main__":
    tl = TrendWriter("asasdadasdasd")
    tl.run()
