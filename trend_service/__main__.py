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

# Add stream handler to logger 'uModbus'.
log_to_stream(level=logging.DEBUG)

# A very simple data store which maps addresses against their values.
data_store = defaultdict(int)

# Enable values to be signed (default is False).
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('', 502), MyRequestHandler.MyRequestHandler)


def main():

    logging.warning('Server started')
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
        logging.warning('Server stopped')


if __name__ == '__main__':
    main()
