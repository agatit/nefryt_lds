from typing import List
import logging
import sqlalchemy as sql

from trend_service.database.orm.TrendData import TrendData

from ..database import Session, engine, orm
from ..database.orm import Trend


def get(trend_id: int, limit: int) -> List[orm.TrendData]:

    try:
        stmt = sql.select([orm.TrendData]) \
            .where(orm.TrendData.TrendID == trend_id) \
            .order_by(orm.TrendData.Time.desc()) \
            .limit(limit)

        result = Session.execute(stmt)
        trend_data = result.fetchall()
        return trend_data

    except Exception as e:
        print(e)
        Session.rollback()
        raise


def insert(trend: orm.Trend, data, time):

    try:
        insert_stmt = sql.insert(orm.TrendData).values(
            TrendID=trend.ID,
            Time=time,
            Data=data
        )

        Session.execute(insert_stmt)
        Session.commit()
    except Exception as e:
        logging.exception(e)
        print(e)
        Session.rollback()
        raise
