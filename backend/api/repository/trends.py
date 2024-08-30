from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db import engine
from database import lds


def get_trends_repository(filter):
    statement = select(lds.Trend)
    # todo: filter
    with Session(engine) as session:
        results = session.execute(statement).all()
        return results


def create_trend_repository(trend):
    with Session(engine) as session:
        session.add(trend)
        session.commit()
        session.refresh(trend)
        return trend
