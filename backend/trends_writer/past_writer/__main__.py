import struct
import sys
import os
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.models import lds
from db import get_engine
import plant
from config import setup_engine

period_start = datetime(2025, 6, 4, 12, 00, 00)
period_end = datetime(2025, 6, 4, 15, 00, 00)
quick_trend_ids = [1, 2, 3, 4]

def read_quick_trend_data(timestamp: int):
    statement = (select(lds.TrendData)
                 .where(lds.TrendData.Time == timestamp) # noqa
                 .where(lds.TrendData.TrendID.in_(quick_trend_ids)))  # noqa
    with Session(get_engine()) as session:
        data = session.execute(statement).fetchall()

    data_dict = dict()
    for row in data:
        data_dict[row[0].TrendID] = struct.unpack("H" * 100, row[0].Data)

    return data_dict


if __name__ == '__main__':
    setup_engine()
    plant = plant.PipePlant(quick_trend_ids)

    ts = int(period_start.timestamp())
    end_ts = int(period_end.timestamp())

    while ts <= end_ts:
        quick_trend_data = read_quick_trend_data(ts)
        plant.update(quick_trend_data, ts)
        ts += 1
