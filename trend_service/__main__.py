#!/usr/bin/env python3
"""Main module of the application."""
import logging
import os
from collections import defaultdict
from socketserver import TCPServer, ThreadingTCPServer

from sqlalchemy import sql
from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

from . import MyRequestHandler
from .database import Session, engine, orm
from .services import (service_trend, service_trend_def, service_trend_param,
                       service_trend_param_def)
# from .trends_writer import TrendWriter

print(__name__)

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# A very simple data store which maps addresses against their values.
data_store = defaultdict(int)

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('', 502), MyRequestHandler.MyRequestHandler)

def main():

    # try:
    trends = service_trend.get_all()
    trend_def = service_trend_def.get_all()
    trend_param = service_trend_param.get_all()
    trend_param_def = service_trend_param_def.get_all()
    
    #  pobranie wszystkich trendow "QUICK"
    quick_trends = service_trend.get_quick_trends()
    
    test = []
    
    for trend in trends:
        print(service_trend.get_all_childs(trend, 'DERIV' ,'TrendID'))
        test.append([trend, service_trend.get_all_childs(trend, 'DERIV' ,'TrendID')])
    
    
    print("alala")
        # trend -> trendefid
        #  if trendefid -> "deriv"
        #  find trendparam where trenparamdefID = trendparam
        
        

    # except Exception as e:
    #     print(e)

    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()


if __name__ == '__main__':
    main()
