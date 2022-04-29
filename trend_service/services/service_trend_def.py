from typing import List

import sqlalchemy as sql

from ..database import Session, engine, orm

__list = []


def __fetch() -> List[orm.TrendDef]:
    stmt = sql.select([orm.TrendDef])
    result = Session.execute(stmt).fetchall()
    for trend in result:
        __list.append(trend[0])

    return get_all()


def get_all() -> List[orm.TrendDef]:
    if( __list == []):
        return __fetch()
    
    return __list


def find_TrendDef(id: int) -> orm.TrendDef:
    for trendDef in get_all():
        if(trendDef.ID == id):
            return trendDef
        
def find_TrendDef(trend: orm.Trend) -> orm.TrendDef:
    for trendDef in get_all():
        if(trendDef.ID == trend.TrendDefID):
            return trendDef

def find_TrendDef_where(trend_def_name: str) -> orm.TrendDef:
    for trendDef in get_all():
        if(trendDef.Name == trend_def_name):
            return trendDef