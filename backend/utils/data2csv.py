from dataclasses import dataclass
import sys
import struct
import itertools
import argparse
import csv
from dateutil import parser
from datetime import datetime


from sqlalchemy import create_engine, alias, select, delete, and_, lambda_stmt
from sqlalchemy.orm import Session

from database.models import lds

# SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo?driver=ODBC+Driver+17+for+SQL+Server'
# SQLALCHEMY_DATABASE_URI = \
#     'mssql+pyodbc://sa:Onyks$us@serverdb:1447/NefrytLDSDemo' \
#     '?driver=ODBC+Driver+18+for+SQL+Server' \
#     '&TrustServerCertificate=Yes' \
#     '&Encrypt=No' 
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://@localhost/NefrytLDS_Zygmuntow_2022?driver=ODBC+Driver+17+for+SQL+Server'


def get_trend_data(session, trend_id_list, begin, end):  # noqa: E501

    # reading trends defnitions neccessary for scaling
    db_trends = session.execute(select(lds.Trend))
    db_trends_scales = {}
    for db_trend, in db_trends:
        db_trends_scales[db_trend.ID] = {
            "RawMin": db_trend.RawMin, 
            "RawMax": db_trend.RawMax, 
            "ScaledMin": db_trend.ScaledMin,
            "ScaledMax": db_trend.ScaledMax
            }

    # preparing result list
    api_data_list = [] # list of data records for all timestames even if there is no data in db
    for timestamp in range(begin, end+1):
        for timestamp_ms in range(0,1000,10):
            api_data_list.append({"Timestamp": timestamp, "TimestampMs": timestamp_ms})

    
    chunk_size = 500 # how many trend points to fetch in one query
    chunk_start = 0

    # for every chunk
    while chunk_start < len(api_data_list):

        # TODO: May be replaces in range in query
        timestamp_list = set()
        for data in itertools.islice(api_data_list, chunk_start, chunk_start + chunk_size):
            timestamp_list.add(data["Timestamp"])

        db_iter = session.execute(
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




if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='data2csv',
        description='Takes data from database and writes to csv file',
        epilog='Happy data crunching :)'
    )

    parser.add_argument('filename', help="desitnation csv file name")
    parser.add_argument('-b', '--begin', help="date and time of beginnig in iso format (e.g. 2024-02-01T12:32:00)", required=True)
    parser.add_argument('-e', '--end', help="date and time of end in iso format (e.g. 2024-02-01T11:17:02)", required=True)
    parser.add_argument('-i', '--ids', help="comma separated list of trend ids to write. If not provided all trends will be written")

    args = parser.parse_args()

    try:
        begin_date = datetime.fromisoformat(args.begin)
        begin_ts = int(begin_date.timestamp())
    except Exception as e:
        print(f"Wrong begin date format {args.begin}: {e}")
        exit(1)

    try:
        end_date = datetime.fromisoformat(args.end)
        end_ts = int(end_date.timestamp())
    except Exception as e:
        print(f"Wrong end date format {args.end}: {e}")
        exit(1)

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    with Session(engine) as session:
        db_trends = session.execute(select(lds.Trend))
        db_trends_ids = [db_trend.ID for db_trend, in db_trends]

    try:
        if args.ids is None:
            ids = db_trends_ids
        else:
            ids = [int(i) for i in args.ids.split(",")]
    except Exception as e:
        print(f"Wrong ids list {args.ids}: {e}")
        exit(1)   

    with Session(engine) as session:
        db_trends = session.execute(select(lds.Trend).where(lds.Trend.ID.in_(ids)))
        db_trends_names = [db_trend.Name for db_trend, in db_trends]         

    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    with Session(engine) as session:
       data = get_trend_data(session, ids, begin_ts, end_ts)

    with open(args.filename, 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONNUMERIC)
        spamwriter.writerow(['Timstamp', 'TimestampMs'] + db_trends_names)
        for row in data:
            spamwriter.writerow(
                [
                    row.get(key,0)
                    for key in ['Timestamp', 'TimestampMs'] + [str(i) for i in ids]
                ]
            )

    print(f"File {args.filename} written")