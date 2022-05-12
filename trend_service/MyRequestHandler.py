from umodbus import log
from umodbus.exceptions import ModbusError, ServerDeviceFailureError
from umodbus.functions import create_function_from_request_pdu
from umodbus.route import Map
from umodbus.server import AbstractRequestHandler, route
from umodbus.server.tcp import RequestHandler
from umodbus.utils import (get_function_code_from_request_pdu,
                           pack_exception_pdu, pack_mbap, recv_exactly,
                           unpack_mbap)

from .services import (service_trend, service_trend_data, service_trend_def,
                       service_trend_param, service_trend_param_def, service_calulcate)


class MyRequestHandler(RequestHandler):
    def __init__(self, request, client_address, server):

        self.trends_const = service_trend.get_all()
        self.trend_def_const = service_trend_def.get_all()
        self.trend_param_const = service_trend_param.get_all()
        self.trend_param_def_const = service_trend_param_def.get_all()

        #  pobranie wszystkich trendow "QUICK" i ich dzieci
        self.quick_trends_const = service_trend.get_quick_trends()
        for quick_trend in self.quick_trends_const:
            service_trend.find_and_add_childs(quick_trend)

        super().__init__(request, client_address, server)

    def process(self, request_adu):
        """ Process request ADU and return response.

        :param request_adu: A bytearray containing the ADU request.
        :return: A bytearray containing the response of the ADU request.
        """
        meta_data = self.get_meta_data(request_adu)

        request_pdu = self.get_request_pdu(request_adu)

        function = create_function_from_request_pdu(request_pdu)
        for quick_trend in self.quick_trends_const:
            if int(quick_trend.params['ModbusRegister']) == function.starting_address:
                quick_trend.save(function.values)
                quick_trend.processData(function.values)
            
        # for quick_trend in self.quick_trends_const:
        #     trend_params = service_trend_param.get_TrendParam_for_specific_trend(
        #         quick_trend.trend, "ModbusRegister")

        #     for trend_param in trend_params:
        #         # and int(trend_param.Value) == 1000:
        #         if trend_param.TrendID == quick_trend.trend.ID and int(trend_param.Value) == function.starting_address:
                    # service_calulcate.calulcate_trend(quick_trend.trend, function)

        response_pdu = function.create_response_pdu()
        response_adu = self.create_response_adu(meta_data, response_pdu)

        return response_adu
