"""Main module of the application."""

import logging
from socketserver import TCPServer, ThreadingTCPServer

from umodbus import conf
from umodbus.server.tcp import RequestHandler, get_server
from umodbus.utils import log_to_stream

from . import MyRequestHandler
from database import session

log_to_stream(level=logging.DEBUG)
conf.SIGNED_VALUES = True

TCPServer.allow_reuse_address = True
app = get_server(TCPServer, ('', 502), MyRequestHandler.MyRequestHandler)

def main():
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()

if __name__ == '__main__':
    main()
