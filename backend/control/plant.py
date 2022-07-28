import logging
from sqlalchemy import select
from .db import global_session
from database import obj

from .drivers import DriverModbus

# TODO: dodać driver Snap7 zamiast AGLink
DRIVER_CLASSES = {
    'TODXModbusTCPDriver': DriverModbus
}

TYPES = [
    "ovtBool","ovtBool8","ovtBool16","ovtBool32","ovtBool64",
    "ovtUint8","ovtUint16","ovtUint32","ovtUint64",
    "ovtInt8","ovtInt16","ovtInt32","ovtInt64",
    "ovtFloat32","ovtFloat48","ovtFloat64","ovtFloat80",
    "ovtString","ovtUnicode","ovtDateTime32", "ovtDateTime64",
    "ovtNull"
]

class Variable:
    def __init__(self, device, alias, address, type) -> None:
        self.device = device
        self.alias = alias
        self.address = address
        self.type = type
        logging.debug(f"Variable {self.device.id} {self.alias} {self.address} created")

    def length(self) -> int:
        """ length in bytes """

        if self.type in ["ovtBool", "ovtBool8", "ovtUint8", "ovtInt8"]:
            return 1
        elif self.type in ["ovtBool16", "ovtUint16", "ovtInt16"]:
            return 2
        elif self.type in ["ovtBool32", "ovtUint32", "ovtInt32", "ovtFloat32", "ovtDateTime32"]:
            return 4
        elif self.type in ["ovtFloat48"]:
            return 6
        elif self.type in ["ovtBool64", "ovtUint64", "ovtInt64, ovtFloat64", "ovtDateTime64"]:
            return 8
        elif self.type in ["ovtFloat80"]:
            return 10
        else:
            return 0
    
    def read(self) -> any:
        return self.device.driver.read(self)

    def write(self, value: any) -> None:
        return self.device.driver.write(self, value)


class Device:
    def __init__(self, id, driver, address) -> None:
        self.varaibles = {}
        self.driver = driver
        self.id = id
        self.address = address
        self._build()
        logging.debug(f"Device {str(id)} {driver.__class__.__name__} {address} created")


    def _build(self) -> None:
        stmt = select(obj.VariableDef) \
            .select_from(obj.Device) \
            .join(obj.VariableDef, obj.Device.DeviceDefID == obj.VariableDef.DeviceDefID) \
            .where(obj.Device.DeviceID == self.id)
        variables = global_session.execute(stmt)
        for variable, in variables:
            self.varaibles[variable.Alias] = Variable(self, variable.Alias, variable.AdressODX, variable.VariableTypeDef.Name)

    def variable(self, key):
        return self.varaibles[key]


class Plant:
    def __init__(self) -> None:
        self.devices = {}
        self.device_symbols = {}
        self.drivers = {}
        self._build()        

    def _build(self) -> None:
        stmt = select(obj.DriverODX)
        drivers = global_session.execute(stmt)
        for driver, in drivers:
            self.drivers[driver.DriverODXID] = DRIVER_CLASSES[driver.DriverClassName](driver.AdressODX, driver.ConnectionString)

        stmt = select(obj.Device)
        devices = global_session.execute(stmt)
        for device, in devices:
            self.devices[device.DeviceID] = Device(device.DeviceID, self.drivers[device.DriverODXID], device.AdressODX)

    def device(self, key):
        return self.devices[key]