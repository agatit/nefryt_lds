#!/usr/bin/env python3
"""Main module of the application."""
import sys
import logging
from collections import defaultdict
from socketserver import TCPServer

from umodbus import conf
from umodbus.server.tcp import get_server
from umodbus.utils import log_to_stream

from .request import MyRequestHandler

def main():

    # log_file_name = 'nefryt_lds_service.log'
    # logging.basicConfig(format='%(asctime)s %(message)s',
    #                     filename=log_file_name, level=logging.INFO)`    

    conf.SIGNED_VALUES = True

    TCPServer.allow_reuse_address = True
    app = get_server(TCPServer, ('', 502), MyRequestHandler)

    logging.info('Server started\n')
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
        logging.info('Server stopped')


if __name__ == '__main__':
    main()
