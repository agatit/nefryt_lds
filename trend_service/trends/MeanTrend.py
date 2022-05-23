import logging
import struct

import numpy as np
from scipy import signal

from ..database import orm
from ..services import service_trend_data
from .CalcTrend import CalcTrend


class MeanTrend(CalcTrend):

    def __init__(self, trend: orm.Trend):
        super().__init__(trend)
        self.window_size = int(self.params['FilterWindow'])

        self.max_values_int16 = np.full(100, fill_value=np.iinfo(np.int16).max)
        self.min_values_int16 = np.full(100, fill_value=np.iinfo(np.int16).min)

        self.storage = np.array([])
        logging.info(self.__class__.__name__ + ": initialized")
        
        self.parent_storage_initiate = False

    def calculate(self, data, parent_id: int = None):

        try:
            # fill storage with data from database to avoid empty storage (lenght of storage is 2*window_size)
            if not self.parent_storage_initiate:
                recent_trend_data_list = service_trend_data.get(
                parent_id, 2*self.window_size/100)
            
                for trend_data in recent_trend_data_list:
                    decoded = list(struct.unpack('<100h', trend_data[0].Data))
                    self.storage = np.append(self.storage, decoded)
                    
                self.parent_storage_initiate = True
            
            
            if len(self.storage) >= 2 * self.window_size + 100:
                kernel = (2 * self.window_size + 1) * [1/self.window_size]
                # norm = 1/(self.window_size*(self.window_size+1))
                result = list(map(int, signal.convolve(
                    self.storage, kernel, mode='valid')))
                self.storage = self.storage[self.window_size:]

                max_cut = np.maximum(result, self.min_values_int16)
                min_cut = np.minimum(max_cut, self.max_values_int16)

                trunced = min_cut

                logging.info(self.__class__.__name__ + ": data calculated")
                return trunced
            else:
                self.storage = np.append(self.storage, data)
        except Exception as e:
            raise e
