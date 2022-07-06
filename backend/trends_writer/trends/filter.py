import struct
from typing import List
import threading
import numpy as np
import logging
from datetime import datetime

from sqlalchemy import select, and_

from database import lds
from ..db import Session
from . import TrendBase
import time


class TrendFilter(TrendBase):

    def __init__(self, id: int, parent_id: int = None):
        super().__init__(id, parent_id)
        self.parent_id = parent_id
        self.window_size = int(self.params['FILTER_WINDOW'])
        self.storage_timstamp = 0
        self.storage = np.array([], dtype=np.uint16)        


    def update(self, data: List[int], timestamp: int, session: Session, parent_id: int = None):

        logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) updating...")

        if parent_id != self.parent_id:
            logging.warning(f"{timestamp} {self.__class__.__name__} ({self.id}) wrong parent id!")
            return None, None

        with self.lock:
            if timestamp == self.storage_timstamp + 1:
                self.storage = np.append(self.storage[100:], np.flip(data))
            elif timestamp > self.storage_timstamp + 1:
                logging.warning(f"{timestamp} {self.__class__.__name__} ({self.id}) data in storage not valid {self.storage_timstamp}")
                self.initiate_buffer(self.window_size, timestamp, session, parent_id)                    
            else:
                logging.warning(f"{timestamp} {self.__class__.__name__} ({self.id}) data in storage alredy exists {self.storage_timstamp}")
                self.storage = np.append(self.storage[:-100], np.flip(data))
        
            self.storage_timstamp = timestamp        

        logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) calculating...")          

        calculated_data = self.calculate()
        if calculated_data is not None:
            super().update(calculated_data, timestamp-self.window_size, session, parent_id)
        else:
            logging.debug(f"{timestamp} {self.__class__.__name__} ({self.id}) empty calculate result")


    def calculate(self) -> np.ndarray:
        raise NotImplementedError


    def initiate_buffer(self, window_size: int, timestamp: int, session: Session, parent_id: int = None):

        # TODO: optymalizacja - ładowanie tylko tych danych których brakuje

        self.storage = np.array([], dtype=np.uint16)

        stmt = select(lds.TrendData) \
            .where(and_(
                lds.TrendData.TrendID == parent_id \
                ,lds.TrendData.Time > timestamp - window_size * 2 - 1 \
                ,lds.TrendData.Time <= timestamp) \
            ).order_by(lds.TrendData.Time.desc()) 

        trend_data_iter = session.execute(stmt)
        trend_data = next(trend_data_iter, None)

        last_valid = 0
        for curr_timestamp in range(timestamp - window_size * 2 - 1, timestamp):
            if trend_data is not None and trend_data[0].Time == curr_timestamp:
                curr_data = struct.unpack('<100h', trend_data[0].Data)
                curr_data = np.flip(curr_data) # ????????
                # fix data
                for i in range(len(curr_data)):
                    if curr_data[i] != 0xFFFF:
                        last_valid = curr_data[i]
                    else:
                        curr_data[i] = last_valid
            else:
                curr_data = np.full(100, fill_value=last_valid, dtype=np.uint16)
                trend_data = next(trend_data_iter, None)
                logging.debug(f"{self.__class__.__name__} ({self.id}) empty trend data")
            self.storage = np.append(self.storage, curr_data)            

        logging.info(f"{self.__class__.__name__} ({self.id}) buffer reads {len(self.storage)} values from {parent_id}")