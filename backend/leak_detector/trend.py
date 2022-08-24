from typing import List
import struct

from sqlalchemy import select, and_

from .db import global_session
from database import lds


class Trend:
    def __init__(self, id, node_id):
        self.id = id
        self.node_id = node_id

    def get_trend_data(self, begin, end) -> List[float]:
        begin = begin // 1000
        end = end // 1000
        # reading trends definitions neccessary for scaling
        trend_def, = global_session.execute(select(lds.Trend).where(lds.Trend.ID == self.id)).fetchone()

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
                if trend_def.RawMin >= 0:
                    one_second_data = reversed(struct.unpack("H"*100, db_data.Data))
                else:
                    one_second_data = reversed(struct.unpack("h"*100, db_data.Data))

                # skalowanie
                for raw_value in one_second_data:
                    last_valid = (trend_def.ScaledMax - trend_def.ScaledMin) \
                                * (raw_value - trend_def.RawMin) \
                                / (trend_def.RawMax - trend_def.RawMin) \
                                + trend_def.ScaledMin
                    data_list.append(last_valid)

                current_timestamp += 1
                                    
            chunk_start += chunk_size

        return data_list
