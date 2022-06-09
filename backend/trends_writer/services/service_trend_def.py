from typing import List

import sqlalchemy as sql

from trends_writer import session
from database.models import lds

__list = []


def __fetch() -> List[lds.TrendDef]:
    stmt = sql.select([lds.TrendDef])
    result = session.execute(stmt).fetchall()
    for trend in result:
        __list.append(trend[0])

    return get_all()


def get_all() -> List[lds.TrendDef]:
    if( __list == []):
        return __fetch()
    
    return __list


def find_TrendDef(id: int) -> lds.TrendDef:
    for trendDef in get_all():
        if(trendDef.ID == id):
            return trendDef
        
def find_TrendDef(trend: lds.Trend) -> lds.TrendDef:
    for trendDef in get_all():
        if(trendDef.ID == trend.TrendDefID):
            return trendDef

def find_TrendDef_where(trend_def_name: str) -> lds.TrendDef:
    for trendDef in get_all():
        if(trendDef.Name == trend_def_name):
            return trendDef