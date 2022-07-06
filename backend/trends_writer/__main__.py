import logging

from trends_writer import app


if __name__ == '__main__':

    logging.info('Server started\n')
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
        logging.info('Server stopped')
