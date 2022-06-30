from umodbus import log
from umodbus.exceptions import ModbusError, ServerDeviceFailureError
from umodbus.functions import create_function_from_request_pdu
from umodbus.route import Map
from umodbus.server import AbstractRequestHandler, route
from umodbus.server.tcp import RequestHandler
from umodbus.utils import (get_function_code_from_request_pdu,
                           pack_exception_pdu, pack_mbap, recv_exactly,
                           unpack_mbap)

from .plant import pipe_plant                           


class ModbusRequest(RequestHandler):
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

        pipe_plant.update(function.starting_address, function.values)

        response_pdu = function.create_response_pdu()
        response_adu = self.create_response_adu(meta_data, response_pdu)

        return response_adu
