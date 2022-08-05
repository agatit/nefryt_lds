import logging

from . import TrendBase


class TrendQuick(TrendBase):

    def __init__(self, id: int, parent_id: int = None):
        super().__init__(id, parent_id)    
        self.register: int = int(self.params['MODBUS_REGISTER'])        
        
