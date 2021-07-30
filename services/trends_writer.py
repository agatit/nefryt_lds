import pyodbc
import threading
import logging
import time
import struct
from datetime import datetime
from socketserver import ThreadingTCPServer
from trends import TrendQuick, TrendDeriv, TrendMean

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

log_to_stream(level=logging.DEBUG)

conf.SIGNED_VALUES = True

serv = get_server(ThreadingTCPServer, ("0.0.0.0", 502 ), RequestHandler)


def get_time_delay():
    return int(time.time()) + 1 - time.time()

class TrendWriter:

    #KAROL: zwraca trend o podanym ID, przydatne dla DERIV i MEAN 
    # bo w bazie danych jest podany nr ID QUICK TREND-U
    def get_trend(self, trend_ID):
        for trend in self.trend_list:
            if trend.get_ID() == int(trend_ID):
                return trend
        return None        

    def __init__(self, connection_string):
        self.connection_string = connection_string


        # buduje listę obiektów odpowiednich klas na podstawie bazy danych
        # inicjalizuje je właściwymi parametrami
        self.trend_list = []
        trend_list_args = []

        #KAROL: tworzę sobie tablicę z wartościami, następnie je zapisuje i tworzę odpowiednio klasy
        con = pyodbc.connect(connection_string, unicode_results = True)
        cur = con.cursor()
        cur.execute("""SELECT 
                        lds.TrendDef.TrendDefID, 
                        lds.TrendDefParam.Value, 
                        lds.TrendDefType.Name 
                    FROM 
                        ((  lds.TrendDef 
                        INNER JOIN lds.TrendDefParam ON (lds.TrendDef.TrendDefID = lds.TrendDefParam.TrendDefID)) 
                        INNER JOIN lds.TrendDefParamDef ON (lds.TrendDefParam.TrendDefParamDefID = lds.TrendDefParamDef.TrendDefParamDefID)) 
                        INNER JOIN lds.TrendDefType ON (lds.TrendDefParamDef.TrendDefTypeID = lds.TrendDefType.TrendDefTypeID) 
                    ORDER BY 
                        lds.TrendDef.TrendDefID, 
                        lds.TrendDefParam.TrendDefParamDefID""")   

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
                trend = TrendDeriv(serv, trend_args[0], self.get_trend(trend_args[1]), trend_args[2])

            elif trend_args[-1] == 'MEAN' : 
                trend = TrendMean(serv, trend_args[0], self.get_trend(trend_args[1]), trend_args[2])

            elif trend_args[-1] == 'QUICK' :
                trend = TrendQuick(serv, *trend_args[0:9])

            self.trend_list.append(trend) 

        con.close()    

    def send_data(self, t):
        threading.Timer(get_time_delay(), self.send_data, args = [t]).start()
        start_time = time.time() 
        timestamp = datetime.utcnow().timestamp()

        if (isinstance(t, TrendDeriv)):
            timestamp = timestamp - t.window_size //100

        if start_time - t.timestamp < 1 : 
            con = pyodbc.connect(self.connection_string, unicode_results = True, autocommit=True)
            cur = con.cursor()
            pack = struct.pack('<100h', * (t.data))
            print("Wysyłam paczke z  sterownika nr" + str(t.trend_ID) + ' o godz UTC:' + str(datetime.fromtimestamp(timestamp)))
            cur.execute("INSERT INTO lds.Trend(TrendDefID, Time, Data) values (?, ?, ?)", t.trend_ID, int(timestamp), pack)
            con.close()         

    def run(self):
        threading.Thread(target = serv.serve_forever).start()
        for t in self.trend_list: 
            if (isinstance(t, TrendQuick)):
                t.run()
                threading.Timer(get_time_delay(), self.send_data, args = [t]).start()

            if (isinstance(t, TrendDeriv)):
                t.run()
                threading.Timer(get_time_delay(), self.send_data, args = [t]).start() 
       

if __name__ == "__main__":

    tl = TrendWriter('DRIVER={SQL Server};SERVER=SERVERDB\MSSQLSERVER2016' + \
                    ';DATABASE=NefrytLDS_NEW' + \
                    ';UID=sa' + \
                    ';PWD=Onyks$us')
    tl.run()            