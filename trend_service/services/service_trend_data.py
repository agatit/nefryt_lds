from typing import List

import sqlalchemy as sql

from ..database import Session, engine, orm
from ..database.orm import Trend


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
