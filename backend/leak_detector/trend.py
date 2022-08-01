from typing import List
import logging
import struct
import itertools

from sqlalchemy import select, insert, and_

from .db import global_session
from database import lds


class Trend:
    def __init__(self, id):
        seld_id = id

    def get_trend_data(self, begin, end) -> List[float]:

        # kod skopiowany z api trends_controller.py z drobnymi zmianami
        # TODO: do poprawy !!!         
        # funkcja ma zawracać wszyskie próbki zdanego zakresu  
        # nie ma potrzeby budowania listy i robienia selectów z "in"          
        # reszta, np podział na chunki, przeliczenia, itp. powinny zostać

        # reading trends defnitions neccessary for scaling
        db_trends = global_session.execute(select(lds.Trend))
        db_trends_scales = {}
        for db_trend, in db_trends:
            db_trends_scales[db_trend.ID] = {
                "RawMin": db_trend.RawMin, 
                "RawMax": db_trend.RawMax, 
                "ScaledMin": db_trend.ScaledMin,
                "ScaledMax": db_trend.ScaledMax
                }

        # readin the trend data
        api_data_list = []

        if samples <= 0:
            samples = 1        
        inc_samples = (100 * (end - begin + 1)) // samples
        if inc_samples == 0:
            inc_samples = 1
        samples = 100 * (end - begin + 1) // inc_samples

        # preparing result list
        last_timestamp = begin
        last_timestamp_samples = 0
        for _ in range(samples):
            api_data_list.append({"Timestamp": last_timestamp, "TimestampMs": last_timestamp_samples * 10})
            last_timestamp += (last_timestamp_samples + inc_samples) // 100
            last_timestamp_samples = (last_timestamp_samples + inc_samples) % 100

        
        chunk_size = 500 # how many trend points to fetch in one query
        chunk_start = 0
    
        # for every chunk
        while chunk_start < len(api_data_list):

            timestamp_list = set()
            for data in itertools.islice(api_data_list, chunk_start, chunk_start + chunk_size):
                timestamp_list.add(data["Timestamp"])        

            db_iter = global_session.execute(
                select(lds.TrendData) \
                    .where(and_(lds.TrendData.Time.in_(timestamp_list), lds.TrendData.TrendID.in_(trend_id_list))) \
                    .order_by(lds.TrendData.Time) 
            )
            api_iter = itertools.islice(api_data_list, chunk_start, chunk_start + chunk_size)

            db_data = next(db_iter, None)
            api_data = next(api_iter, None)
                    
            while db_data and api_data:              
                while db_data[0].Time < api_data["Timestamp"]:
                    db_data = next(db_iter)

                one_second_data = {}
                while db_data and db_data[0].Time == api_data["Timestamp"]:
                    if db_trends_scales[db_data[0].TrendID]["RawMin"] >= 0:
                        one_second_data[db_data[0].TrendID] = struct.unpack("H"*100, db_data[0].Data)
                    else:
                        one_second_data[db_data[0].TrendID] = struct.unpack("h"*100, db_data[0].Data)
                    db_data = next(db_iter, None)

                current_second = api_data["Timestamp"]
                while api_data and api_data["Timestamp"] == current_second:
                    for trend_id in one_second_data.keys():
                        api_data[str(trend_id)] = \
                            (db_trends_scales[trend_id]["ScaledMax"] - db_trends_scales[trend_id]["ScaledMin"]) \
                            * (one_second_data[trend_id][-api_data["TimestampMs"]//10-1] - db_trends_scales[trend_id]["RawMin"]) \
                            / (db_trends_scales[trend_id]["RawMax"] - db_trends_scales[trend_id]["RawMin"]) \
                            + db_trends_scales[trend_id]["ScaledMin"]
                    api_data = next(api_iter, None)
                                    
            chunk_start += chunk_size

        return api_data_list
