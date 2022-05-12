# import logging
# import struct
# # import pyodbc
# import threading
# import time
# from datetime import datetime
# from socketserver import ThreadingTCPServer

# from sqlalchemy import and_
# from sqlalchemy.sql import text
# from umodbus import conf
# from umodbus.server.tcp import RequestHandler, get_server

# from .database import Session, engine, orm
# from .trends import TrendDeriv, TrendMean, TrendQuick


# def get_utc_timestamp(local_timestamp):
#     return datetime.utcfromtimestamp(local_timestamp).timestamp()


# class TrendWriter:

#     def get_trend(self, trend_ID):
#         for trend in self.trend_list:
#             if trend.get_ID() == int(trend_ID):
#                 return trend
#         return None

#     def __init__(self, connection_string):
#         conf.SIGNED_VALUES = True

#         self.connection_string = connection_string
#         self.terminate = False
#         # https://stackoverflow.com/questions/24001147/python-bind-socket-error-errno-13-permission-denied
#         self.serv = get_server(
#             ThreadingTCPServer, ("0.0.0.0", 1024), RequestHandler)
#         self.serv.daemon_threads = True
#         self.trend_list = []
#         trend_list_args = []

#         from sqlalchemy import sql
#         query = sql.select([orm.Trend.ID.label('TrendID'),
#                             orm.TrendParam.Value.label('Value'),
#                             # orm.TrendParamDef.Name.label('Name')
#                             orm.TrendDef.Name.label('Name')
#                             ]) \
#             .join(orm.TrendDef, orm.TrendDef.ID == orm.Trend.TrendDefID, isouter=True) \
#             .join(orm.TrendParamDef, orm.TrendDef.ID == orm.TrendParamDef.TrendDefID, isouter=True) \
#             .join(orm.TrendParam,
#                   and_(
#                       orm.TrendParamDef.ID == orm.TrendParam.TrendParamDefID,
#                       orm.TrendParam.TrendID == orm.Trend.ID), isouter=True)
#         # print(query)

#         rows = Session.execute(query).fetchall()

#         for trend_args in rows:
#             print(trend_args)
#             print(trend_args[-1])

#             trend = None

#             if trend_args[-1] == 'DERIV':
                # trend = TrendDeriv(self.serv, trend_args[0], self.get_trend(
                #     trend_args[1]), trend_args[2])

#             elif trend_args[-1] == 'MEAN':
#                 trend = TrendMean(self.serv, trend_args[0], self.get_trend(
#                     trend_args[1]), trend_args[2])

#             elif trend_args[-1] == 'QUICK':
#                 trend = TrendQuick(self.serv, *trend_args[0:9])

#             if trend:
#                 self.trend_list.append(trend)

#     def send_data(self, trend):
#         print("Sending data for trend {}".format(trend.get_ID()))
#         pass
#         # data = trend.data
#         # timestamp = trend.timestamp

#         # if self.terminate:
#         #     trend.terminate = True
#         #     return

#         # now = int(trend.send_next_tick)
#         # trend.send_next_tick = trend.send_next_tick + 1
#         # threading.Timer(trend.send_next_tick - time.time(), self.send_data, args = [trend]).start()
#         # N = trend.window_size // 100 + 1

#         # if timestamp and not None in data and (now - timestamp == 1 or not isinstance(trend, TrendQuick)):

#         #     try:
#         #         con = pyodbc.connect(self.connection_string, unicode_results = True, autocommit=True)
#         #         cur = con.cursor()
#         #         pack = struct.pack('<100h', *data)
#         #         cur.execute("INSERT INTO lds.Trend(TrendDefID, Time, Data) values (?, ?, ?)",
#         #                  trend.trend_ID, get_utc_timestamp(now - N), pack)
#         #         con.close()
#         #         return

#         #     except pyodbc.IntegrityError:
#         #         logging.error("Integrity Error. The record already exist.")
#         #         return

#         #     except pyodbc.Error:
#         #         logging.error("Lost Database Connection.")
#         #         return

#         # if timestamp and not None in data and now - timestamp == 1 :
#         #     logging.info("Wrong timestamp.")
#         #     return

#     def run(self):
#         time.sleep(int(time.time()) + 1 - time.time())
#         for trend in self.trend_list:
#             threading.Timer(trend.run_next_tick -
#                             time.time(), trend.run).start()
#             threading.Timer(trend.send_next_tick - time.time(),
#                             self.send_data, args=[trend]).start()

#         self.serv.serve_forever()

#     def stop(self):
#         self.terminate = True
#         self.serv.shutdown()
#         self.serv.server_close()


# if __name__ == '__main__':
#     t = TrendWriter('DRIVER={SQL Server}' +
#                     ';SERVER=SERVERDB,1447' +
#                     ';DATABASE=NefrytLDSDemo' +
#                     ';UID=sa' +
#                     ';PWD=Onyks$us')
#     t.run()
