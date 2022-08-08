from socketserver import TCPServer

import umodbus
import umodbus.server.tcp
from umodbus.functions import create_function_from_request_pdu

from .config import config                        


class ModbusRequest(umodbus.server.tcp.RequestHandler):
    pipe_plant = None

    def __init__(self, request, client_address, server):

        super().__init__(request, client_address, server)


    def process(self, request_adu):
        """ Process request ADU and return response.

        :param request_adu: A bytearray containing the ADU request.
        :return: A bytearray containing the response of the ADU request.
        """
        meta_data = self.get_meta_data(request_adu)
        request_pdu = self.get_request_pdu(request_adu)
        function = create_function_from_request_pdu(request_pdu)

        self.pipe_plant.update(function.starting_address, function.values)

        response_pdu = function.create_response_pdu()
        response_adu = self.create_response_adu(meta_data, response_pdu)

        return response_adu


def get_server(pipe_plant):
    umodbus.conf.SIGNED_VALUES = True
    TCPServer.allow_reuse_address = True

    ModbusRequest.pipe_plant = pipe_plant

    app = umodbus.server.tcp.get_server(TCPServer, ('', config.get("modbus_port", 502)), ModbusRequest)

    return app

