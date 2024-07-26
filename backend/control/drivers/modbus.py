from typing import List
import re
import struct
import logging
import socket
import numpy as np

from umodbus import conf
from umodbus.client import tcp

TYPE_FORMAT = {
    "ovtBool": '<B',
    "ovtBool8": '<B',
    "ovtBool16": '<H',
    "ovtBool32": '<I',
    "ovtBool64": '<Q',
    "ovtUint8": '<B',
    "ovtUint16": '<H',
    "ovtUint32": '<I',
    "ovtUint64": '<Q',
    "ovtInt8": '<b',
    "ovtInt16": '<h',
    "ovtInt32": '<i',
    "ovtInt64": '<q',
    "ovtFloat32": '<f',
    "ovtFloat48": '<d',
    "ovtFloat64": '<d',
    "ovtFloat80": '<q',
    # "ovtString": ,
    # "ovtUnicode": ,
    "ovtDateTime32": '<I',
    "ovtDateTime64": '<Q'
    # "ovtNull"" 
}



class DriverModbus:

    def __init__(self, address, connecion_string):
        self.config = {}
        self.address = address
        self.connecion_string = connecion_string # e.g.: HostName=192.168.18.32, PortNo=502, UseZeroBaseAddressing=False, SlaveID=1

        params = re.split(r'[,; ]+', self.connecion_string)
        for param in params:
            key, value = re.split('[= ]+', param, 1)
            self.config[key] = value

        self.host_name = self.config['HostName']
        self.port_no = int(self.config['PortNo'])
        self.slave_id = int(self.config['SlaveID'])
        self.use_zero_base_addressing = bool(self.config['UseZeroBaseAddressing'])

        conf.SIGNED_VALUES = False

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host_name, 502))     


    def _get_address(self, variable):

        res = re.search(r'^([14])(\d+)\.?(\d*)', self.address)
        if res is not None:
            prefix, driver_register, driver_bit = res.groups()
        else:
            prefix, driver_register, driver_bit = 4, 0, 0
        if driver_bit == '':
            driver_bit = 0

        res = re.search(r'^(\d+)\.?(\d*)', variable.address)
        variable_register, variable_bit = res.groups()   
        if variable_bit == '':
            variable_bit = 0

        res = re.search(r'^(\d+)\.?(\d*)',  variable.device.address)
        device_register, device_bit = res.groups()
        if device_bit == '':
            device_bit = 0

        register = int(driver_register) + int(variable_register) + int(device_register)
        bit = int(driver_bit) + int(variable_bit) + int(device_bit)

        return prefix, register, bit


    def _value_to_registers(self, value, type, bit=0) -> List[np.uint16]:
            
        registers: List[np.uint16] = []

        if type in ["ovtBool", "ovtBool8", "ovtBool16", "ovtBool32", "ovtBool64"]:
            if value:
                data = value << bit
            else:
                data = ~(value << bit)
        else:
            data = value                
        format = TYPE_FORMAT[type] *  self.length(type)
        registers = list(struct.unpack( format, struct.pack(TYPE_FORMAT[type], data)))

        return registers


    def _registers_to_value(self, registers, type,  bit=0):

        format = TYPE_FORMAT[type] *  self.length(type)
        value = struct.unpack( TYPE_FORMAT[type], struct.pack(format, *registers) )[0]

        if type in ["ovtBool", "ovtBool8", "ovtBool16", "ovtBool32", "ovtBool64"]:
            if (value >> bit & 1) == 1:
                value = True
            else:
                value = False
        else:
            return value              



    def length(self, type: str) -> int:
        """ length in registers """

        if type in ["ovtBool", "ovtBool8", "ovtUint8", "ovtInt8", "ovtBool16", "ovtUint16", "ovtInt16"]:
            return 1
        elif type in ["ovtBool32", "ovtUint32", "ovtInt32", "ovtFloat32", "ovtDateTime32"]:
            return 2
        elif type in ["ovtFloat48"]:
            return 3
        elif type in ["ovtBool64", "ovtUint64", "ovtInt64, ovtFloat64", "ovtDateTime64"]:
            return 4
        elif type in ["ovtFloat80"]:
            return 5
        else:
            return 0    


    def read(self, variable):
        prefix, register, bit = self._get_address(variable)        
        logging.info(f"Modbus read register: {register}.{bit}")

        # TODO: obłsuzyć i przetestować inne funkcje
        if prefix == "4":
            req_adu = tcp.read_holding_registers(self.slave_id, register, self.length(variable.type))
            response = tcp.send_message(req_adu, self.sock)
            return self._registers_to_value(response, variable.type, bit)


    def write(self, variable, value: any):
        prefix, register, bit = self._get_address(variable)
        logging.info(f"Modbus write register: {register}.{bit}")

        # TODO: obłsuzyć i przetestować inne funkcje
        if prefix == "4":
            registers = self._value_to_registers(value, variable.type, bit)
            req_adu = tcp.write_multiple_registers(self.slave_id, register, registers)
            response = tcp.send_message(req_adu, self.sock)
            return response       