import logging
import threading
import time
import struct
from datetime import datetime

import pymssql
from socketserver import ThreadingTCPServer
from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server

from trends import TrendQuick, TrendDeriv, TrendMean

class Writer:


    def get_trend(self, trend_ID):
        for trend in self.trend_list:
            if trend.get_ID() == int(trend_ID):
                return trend
        return None        


    def __init__(self, connection_string):
        conf.SIGNED_VALUES = True

        self.connection_string = connection_string
        self.terminate = False
        self.serv = get_server(ThreadingTCPServer, ("0.0.0.0", 502 ), RequestHandler)
        self.serv.daemon_threads = True
        self.trend_list = []
        trend_list_args = []

        try:
            con = pymssql.connect(connection_string, unicode_results = True)
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

            con.close()

        except pymssql.Error:
            logging.fatal("No database connection.") 

          
        for trend_args in trend_list_args:

            if trend_args[-1] == 'DERIV' :
                trend = TrendDeriv(self.serv, trend_args[0], self.get_trend(trend_args[1]), trend_args[2])

            elif trend_args[-1] == 'MEAN' : 
                    trend = TrendMean(self.serv, trend_args[0], self.get_trend(trend_args[1]), trend_args[2])

            elif trend_args[-1] == 'QUICK' :
                trend = TrendQuick(self.serv, *trend_args[0:9])

            self.trend_list.append(trend) 

    def send_data(self, trend):
        data = trend.data
        timestamp = trend.timestamp

        if self.terminate:
            trend.terminate = True
            return

        now = int(trend.send_next_tick)
        trend.send_next_tick = trend.send_next_tick + 1
        threading.Timer(trend.send_next_tick - time.time(), self.send_data, args = [trend]).start()
        N = trend.window_size // 100 + 1

        if timestamp and not None in data and (now - timestamp == 1 or not isinstance(trend, TrendQuick)):
            
            try:
                con = pymssql.connect(self.connection_string, unicode_results = True, autocommit=True)
                cur = con.cursor()
                pack = struct.pack('<100h', *data)
                cur.execute("INSERT INTO lds.Trend(TrendDefID, Time, Data) values (?, ?, ?)",
                         trend.trend_ID, datetime.get_utc_timestamp(now - N), pack)
                con.close()
                return

            except pymssql.IntegrityError:
                logging.error("Integrity Error. The record already exist.")
                return
            
            except pymssql.Error:
                logging.error("Lost Database Connection.")
                return
        
        if timestamp and not None in data and now - timestamp == 1 :
            logging.info("Wrong timestamp.")
            return
        

    def run(self):
        time.sleep( int(time.time()) + 1 - time.time())
        for trend in self.trend_list:
            threading.Timer(trend.run_next_tick - time.time(), trend.run).start()
            threading.Timer(trend.send_next_tick - time.time(), self.send_data, args = [trend]).start()

        self.serv.serve_forever()


    def stop(self):
        self.terminate = True
        self.serv.shutdown()
        self.serv.server_close()