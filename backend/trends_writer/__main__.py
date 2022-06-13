#!/usr/bin/env python3
"""Main module of the application."""
import logging
from collections import defaultdict
from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import get_server
from umodbus.utils import log_to_stream

from . import MyRequestHandler

print(__name__)
log_file_name = 'nefryt_lds_service.log'
logging.basicConfig(format='%(asctime)s %(message)s',
                    filename=log_file_name, level=logging.INFO)

log_to_stream(level=logging.DEBUG)
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('', 502), MyRequestHandler.MyRequestHandler)


def main():

    logging.info('Server started')
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
        logging.info('Server stopped')


# def drawing():
#     from matplotlib import pyplot as plt
#     from .services import service_trend
#     from .services import service_trend_data
#     import struct
#     import numpy as np
#     # pobranie wszystkich trendow "QUICK" i ich dzieci
#     quick_trends_const = service_trend.get_quick_trends()

#     for quick_trend in quick_trends_const:
#         service_trend.find_and_add_childs(quick_trend)

#     tuple_timestamp_trendID_data = []
#     for quick_trend in quick_trends_const:
#         for child in quick_trend.children:
#             if child.trend.TrendDefID.strip() == 'DERIV':
#                 child_id = child.trend.ID
#                 recent_trend_data_list = service_trend_data.get(
#                     child_id, int(child.params['FilterWindow']) / 10)
#                 for trend_data in recent_trend_data_list:
#                     tuple_timestamp_trendID_data.append((child_id, trend_data[0].Time, np.array(
#                         struct.unpack('<100h', trend_data[0].Data))))

#     for tuple in tuple_timestamp_trendID_data:
#         l = len(tuple[2])
#         r = np.arange(l)
#         plt.plot(r, tuple[2])

#     plt.savefig(f"foo1.png")

if __name__ == '__main__':
    # drawing()
    
    main()
