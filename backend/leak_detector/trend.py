from typing import List
import logging
import struct
import itertools

from sqlalchemy import select, insert, and_

from .db import global_session
from database import lds


class Trend:
    def __init__(self, id):
        self.id = id

    #sprawdzić, czy działa zbieranie trendów / czy się nie da jeszcze bardziej uprościć

    def get_trend_data(self, begin, end) -> List[float]:

        # kod skopiowany z api trends_controller.py z drobnymi zmianami
        # TODO: do poprawy !!!
        # funkcja ma zawracać wszyskie próbki z danego zakresu
        # nie ma potrzeby budowania listy i robienia selectów z "in"
        # reszta, np podział na chunki, przeliczenia, itp powinny zostać

        # reading trends definitions neccessary for scaling
        db_trends = global_session.execute(select(lds.Trend))
        db_trends_scales = {}
        for db_trend, in db_trends:
            db_trends_scales[db_trend.ID] = {
                "RawMin": db_trend.RawMin, 
                "RawMax": db_trend.RawMax, 
                "ScaledMin": db_trend.ScaledMin,
                "ScaledMax": db_trend.ScaledMax
            }

        timestamps = list(range(begin, end + 1))            
        chunk_size = 500 # how many trend points to fetch in one query
        chunk_start = 0
    
        data_list = []

        # for every chunk
        while chunk_start < len(timestamps):

            timestamp_list = set()
            for data in itertools.islice(timestamps, chunk_start, chunk_start + chunk_size):
                timestamp_list.add(data)        

            db_iter = global_session.execute(
                select(lds.TrendData) \
                    .where(and_(lds.TrendData.Time.in_(timestamp_list), lds.TrendData.TrendID == self.id)) \
                    .order_by(lds.TrendData.Time) 
            )
            timestamp_iter = itertools.islice(timestamps, chunk_start, chunk_start + chunk_size)

            db_data = next(db_iter, None)
            timestamp_data = next(timestamp_iter, None)
                    
            while db_data and timestamp_data:              
                while db_data[0].Time < timestamp_data:
                    db_data = next(db_iter)

                one_second_data = {}
                while db_data and db_data[0].Time == timestamp_data:
                    if db_trends_scales[db_data[0].TrendID]["RawMin"] >= 0:
                        one_second_data[db_data[0].TrendID] = struct.unpack("H"*100, db_data[0].Data)
                    else:
                        one_second_data[db_data[0].TrendID] = struct.unpack("h"*100, db_data[0].Data)
                    db_data = next(db_iter, None)

                current_second = timestamp_data
                while timestamp_data and timestamp_data == current_second:
                    for trend_id in one_second_data.keys():
                        data_list.append(
                            (db_trends_scales[trend_id]["ScaledMax"] - db_trends_scales[trend_id]["ScaledMin"]) \
                            * (one_second_data[trend_id][-1] - db_trends_scales[trend_id]["RawMin"]) \
                            / (db_trends_scales[trend_id]["RawMax"] - db_trends_scales[trend_id]["RawMin"]) \
                            + db_trends_scales[trend_id]["ScaledMin"])
                    timestamp_data = next(timestamp_iter, None)
                                    
            chunk_start += chunk_size
                
        return data_list
