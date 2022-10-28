from datetime import datetime
import logging
from typing import List
import struct

from sqlalchemy import select, and_

from .db import global_session
from database import lds


class Trend:
    def __init__(self, id: int, node_id: int):
        self.id = id
        self.node_id = node_id
        self.params = {}
        self.get_params()
        logging.debug(f"Trend {self.id} {self.node_id} created")

    def get_params(self):
        stmt = select([lds.TrendParam, lds.TrendParamDef]) \
                .select_from(lds.TrendParamDef) \
                .where(lds.TrendParam.TrendID == self.id) \
                .outerjoin(lds.TrendParam, \
                    and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID, lds.TrendParam.TrendID == self.id) \
                )
        for param, param_def in global_session.execute(stmt):
           if param is not None:
                self.params[param_def.ID.strip()] = float(param.Value)
        

    def get_trend_data(self, begin: int, end: int) -> List[float]:
        begin = begin // 1000
        end = end // 1000
        logging.debug(f"Get data from {datetime.fromtimestamp(begin)} to {datetime.fromtimestamp(end)}.")
        # reading trends definitions neccessary for scaling

        last_valid = 0 # ostatnia prawidłowa wartość - do wypełniania pól z wartościami nieprawidływmi 
        chunk_size = 500 # how many trend points to fetch in one query
        chunk_start = begin
    
        data_list = []

        # for every chunk
        while chunk_start <= end:
     
            db_iter = global_session.execute(
                select(lds.TrendData) \
                    .where(and_(lds.TrendData.Time >= chunk_start, lds.TrendData.Time < min(chunk_start+chunk_size, end), lds.TrendData.TrendID == self.id)) \
                    .order_by(lds.TrendData.Time) 
            )            
            current_timestamp = chunk_start

            for db_data, in db_iter:
                while current_timestamp < db_data.Time:
                    data_list += [last_valid] * 100
                    current_timestamp += 1

                # rozpoznajemy czy dane sa signed czy unsigned
                if self.params['RAW_MIN'] >= 0:
                    one_second_data = reversed(struct.unpack("H"*100, db_data.Data))
                else:
                    one_second_data = reversed(struct.unpack("h"*100, db_data.Data))

                # skalowanie
                for raw_value in one_second_data:
                    last_valid = (self.params['SCALED_MAX'] - self.params['SCALED_MIN']) \
                                * (raw_value - self.params['RAW_MIN']) \
                                / (self.params['RAW_MAX'] - self.params['RAW_MIN']) \
                                + self.params['SCALED_MIN']

                    last_valid = - last_valid * (last_valid < 0)
                    
                    data_list.append(last_valid)

                current_timestamp += 1
                                    
            chunk_start += chunk_size
        logging.debug(f"Got data successfully.")
        return data_list
