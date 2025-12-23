import logging
import struct
import sys
import os
from argparse import ArgumentParser
from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from database.models import lds
from db import get_engine
from . import plant
from config import setup_engine

logger = logging.getLogger('trends_writer.past_writer')


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
    argparser = ArgumentParser()
    argparser.add_argument("--quick_trend_ids", type=int, required=False, default=quick_trend_ids, nargs='+')
    argparser.add_argument("--from_timestamp", type=int, required=False, default=int(period_start.timestamp()))
    argparser.add_argument("--to_timestamp", type=int, required=False, default=int(period_end.timestamp()))
    args = argparser.parse_args()

    setup_engine()
    plant = plant.PipePlant(quick_trend_ids)

    ts = args.from_timestamp
    end_ts = args.to_timestamp
    quick_trend_ids = args.quick_trend_ids

    logger.info(f'PastWriter: Module started in period {ts}-{end_ts} for trends = {quick_trend_ids}')
    while ts <= end_ts:
        quick_trend_data = read_quick_trend_data(ts)
        plant.update(quick_trend_data, ts)
        ts += 1
    logger.info(f'PastWriter: Module finished')
