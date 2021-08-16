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

def get_utc_timestamp(local_timestamp):
    return datetime.utcfromtimestamp(local_timestamp).timestamp()

class TrendWriter:
    
    def get_trend(self, trend_ID):
        for trend in self.trend_list:
            if trend.get_ID() == int(trend_ID):
                return trend
        return None        

    def __init__(self, connection_string):
        self.connection_string = connection_string

        self.trend_list = []
        trend_list_args = []

        try:
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

        except pyodbc.Error :
            logging.error("Brak połączenia z bazą danych.") 

    def send_data(self, trend):
        data = trend.data
        timestamp = trend.timestamp
        now = int(trend.send_next_tick)
        trend.send_next_tick = trend.send_next_tick + 1
        threading.Timer(trend.send_next_tick - time.time(), self.send_data, args = [trend]).start()
        N = trend.window_size // 100 + 1

        if timestamp and not None in data and (now - timestamp == 1 or isinstance(trend, TrendDeriv) ):
            
            try:
                con = pyodbc.connect(self.connection_string, unicode_results = True, autocommit=True)
                cur = con.cursor()
                pack = struct.pack('<100h', *data)
                cur.execute("INSERT INTO lds.Trend(TrendDefID, Time, Data) values (?, ?, ?)",
                         trend.trend_ID, get_utc_timestamp(now - N), pack)
                con.close()

            except pyodbc.IntegrityError:
                 logging.error("Próba wstawienia rekordu, który już istnieje.")

            except pyodbc.Error:
                logging.error("Brak połączenia z serwerem")


    def run(self):
        threading.Thread(target = serv.serve_forever).start()
        for trend in self.trend_list:
            if isinstance(trend, TrendQuick) : 
                threading.Timer(trend.send_next_tick - time.time(), trend.run).start()
                threading.Timer(trend.send_next_tick - time.time(), self.send_data, args = [trend]).start()

            if isinstance(trend, TrendDeriv) : 
                threading.Timer(trend.run_next_tick - time.time(), trend.run).start()
                threading.Timer(trend.send_next_tick - time.time(), self.send_data, args = [trend]).start()

if __name__ == "__main__":
    time.sleep(int(time.time()) + 1 - time.time())
    tl = TrendWriter('DRIVER={SQL Server};SERVER=192.168.18.11' + \
                     ';DATABASE=NefrytLDS_NEW' + \
                     ';UID=sa' + \
                     ';PWD=Onyks$us')
    tl.run()