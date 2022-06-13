from typing import List
import logging

import sqlalchemy as sql
from trends_writer import session
from database import lds


def get(trend_id: int, limit: int) -> List[lds.TrendData]:

    try:
        stmt = sql.select([lds.TrendData]) \
            .where(lds.TrendData.TrendID == trend_id) \
            .order_by(lds.TrendData.Time.desc()) \
            .limit(limit)

        result = session.execute(stmt)
        trend_data = result.fetchall()
        return trend_data

    except Exception as e:
        print(e)
        session.rollback()
        raise


def insert(trend: lds.Trend, data, time):

    try:
        insert_stmt = sql.insert(lds.TrendData).values(
            TrendID=trend.ID,
            Time=time,
            Data=data
        )

        session.execute(insert_stmt)
        session.commit()
    except Exception as e:
        logging.exception(e)
        print(e)
        session.rollback()
        raise
