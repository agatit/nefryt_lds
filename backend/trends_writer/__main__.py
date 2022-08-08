import logging
from . import modbus
from . import plant


if __name__ == '__main__':


    app = modbus.get_server(plant.PipePlant())

    logging.info('Server started\n')
    try:
        app.serve_forever()
    finally:
        app.shutdown()
        app.server_close()
        logging.info('Server stopped')
