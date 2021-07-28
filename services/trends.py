import threading
import pyodbc
import time

#KAROL: każda klasa ma przynajmniej jeden argument i jest to Trend_ID
class Trend:
    def get_ID(self):
        return int(self.trend_ID)

    def __init__(self, trend_ID):
        self.trend_ID = trend_ID
        pass

    def run(self):
        pass


class TrendQuick(Trend):
    # powinien uruchamiać wątki serwera modbus
    def __init__(self, trend_ID, host_name, port, slave_ID,
                register, raw_min, raw_max, scaled_min, scaled_max ):
        super().__init__(trend_ID)
        self.host_name = host_name
        self.port = port
        self.slave_ID = slave_ID
        self.register = register
        self.raw_min = raw_min
        self.raw_max = raw_max
        self.scaled_min = scaled_min
        self.scaled_max = scaled_max

    def send_data(self):
        threading.Timer(1, self.send_data).start()
        #KAROL: wysyła dane do bazy danych, do zrobienia


    def run(self):
        threading.Timer(1, self.send_data).start()

    def __str__(self):
        return str(self.host_name) + ', ' +  str(self.port) + ', ' + str(self.slave_ID) + '...'    


class TrendDeriv(Trend):
    # powinien uruchamiać wątek przeliczający, parametrem konstruktora powinien być TrendQuick
    # powinien utrzymywać bufor wartości i uzupełniać ją wartościami z quick trendu
    def __init__(self, trend_ID, trend_quick, window_size):
        super().__init__(trend_ID)
        self.trend_quick = trend_quick
        self.window_size = window_size

    def __str__(self):
        return str(self.trend_ID) + ", " +  str(self.trend_quick)


class TrendMean(Trend):
    # j.w.
    def __init__(self, trend_ID,  trend_quick, window_size):
        super().__init__(trend_ID)
        self.trend_quick = trend_quick
        self.window_size = window_size
        pass

    def __str__(self):
        return str(self.trend_ID) + ", " +  str(self.trend_quick)

class TrendWriter:

    #KAROL: zwraca trend o podanym ID, przydatne dla DERIV i MEAN 
    # bo w bazie danych jest podany nr ID QUICK TREND-U
    def get_trend(self, trend_ID):
        for trend in self.trend_list:
            if trend.get_ID() == int(trend_ID):
                return trend
        return None        


    def __init__(self, connection_string):
        # buduje listę obiektów odpowiednich klas na podstawie bazy danych
        # inicjalizuje je właściwymi parametrami
        self.trend_list = []
        trend_list_args = []

        #KAROL: tworzę sobie tablicę z wartościami, następnie je zapisuje i tworzę odpowiednio klasy
        con = pyodbc.connect(connection_string, unicode_results = True)
        cur = con.cursor()
        cur.execute("SELECT \
                        lds.TrendDef.TrendDefID, \
                        lds.TrendDefParam.Value, \
                        lds.TrendDefType.Name \
                    FROM \
                    ((  lds.TrendDef \
                    INNER JOIN lds.TrendDefParam ON (lds.TrendDef.TrendDefID = lds.TrendDefParam.TrendDefID)) \
                    INNER JOIN lds.TrendDefParamDef ON (lds.TrendDefParam.TrendDefParamDefID = lds.TrendDefParamDef.TrendDefParamDefID)) \
                    INNER JOIN lds.TrendDefType ON (lds.TrendDefParamDef.TrendDefTypeID = lds.TrendDefType.TrendDefTypeID) \
                    ORDER BY \
                    lds.TrendDef.TrendDefID, \
                    lds.TrendDefParam.TrendDefParamDefID")   

        row = cur.fetchone()
        while row:
            args = [row[0]]
            trend_type = row[2]

            while row and row[0] == args[0]:
                args.append(row[1])
                row = cur.fetchone()

            trend_list_args.append([*args, trend_type])       
        
        for trend_args in trend_list_args:

            if trend_args[-1] == 'DERIV' :
                trend = TrendDeriv(trend_args[0], self.get_trend(trend_args[1]), 0)

            elif trend_args[-1] == 'MEAN' : 
                trend = TrendMean(trend_args[0], self.get_trend(trend_args[1]), 0)

            elif trend_args[-1] == 'QUICK' :
                trend = TrendQuick(*trend_args[0:9])

            self.trend_list.append(trend) 

        con.close()    


    def run(self):
        for t in self.trend_list:
            print(t) #t.run() tu będzie 

if __name__ == "__main__":

    tl = TrendWriter('DRIVER={SQL Server};SERVER=SERVERDB\MSSQLSERVER2016' + \
                    ';DATABASE=NefrytLDS_NEW' + \
                    ';UID=sa' + \
                    ';PWD=Onyks$us')
    tl.run()