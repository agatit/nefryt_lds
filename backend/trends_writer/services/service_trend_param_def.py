from typing import List

import sqlalchemy as sql

from trends_writer import session
from database.models import lds

__list = []


def __fetch() -> List[lds.TrendParamDef]:
    stmt = sql.select([lds.TrendParamDef])
    result = session.execute(stmt).fetchall()
    for trend in result:
        __list.append(trend[0])

    return get_all()


def get_all() -> List[lds.TrendParamDef]:
    if( __list == []):
        return __fetch()
    
    return __list


def get_all_TrendParamDef_where_name_is(name: str) -> List[lds.TrendParamDef]:
    __list_of_trend_param_def = []

    for item in __list:
        if item.Name == name:
            __list_of_trend_param_def.append(item)

    return __list_of_trend_param_def

def get_all_TrendParamDef_where(id: int) -> List[lds.TrendParamDef]:
    __list_of_trend_param_def = []

    for item in __list:
        if item.Name == id:
            __list_of_trend_param_def.append(item)

    return __list_of_trend_param_def