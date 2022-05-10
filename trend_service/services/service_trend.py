from typing import List

import sqlalchemy as sql
from sqlalchemy import and_

from ..database import Session, engine, orm
from . import service_trend_def, service_trend_param_def

__list = []

# class TrendService():
#     def __init__(self):
#         pass


def __fetch() -> List[orm.Trend]:
    stmt = sql.select([orm.Trend])
    result = Session.execute(stmt).fetchall()
    for trend in result:
        __list.append(trend[0])

    return get_all()


def get_all() -> List[orm.Trend]:
    if(__list == []):
        return __fetch()

    return __list


def find_child_of_trend(trend: orm.Trend, trend_def_name: str, trend_param_def_name: str) -> orm.Trend:

    if trend is None:
        return None

    trend_def = service_trend_def.find_TrendDef_where(trend_def_name)

    if trend_def is None:
        return None

    if trend_def.ID != trend.TrendDefID:
        return None

    stmt = sql.select([orm.TrendParamDef]) \
        .where(and_(orm.TrendParamDef.Name == trend_param_def_name, orm.TrendParamDef.TrendDefID == trend.TrendDefID))

    print(stmt)

    trend_param_def = Session.execute(stmt).fetchone()
    # print(trend_param_def)
    if (trend_param_def == None):
        return None

    trend_param_def = trend_param_def[0]
    print(trend_param_def)
    stmt = sql.select([orm.TrendParam]) \
        .where(and_(orm.TrendParam.TrendParamDefID == trend_param_def.ID,
                    orm.TrendParam.TrendID == trend.ID))

    trend_param = Session.execute(stmt).fetchone()

    if (trend_param == None):
        return None

    print(trend_param)

    trend_param = trend_param[0]

    stmt = sql.select([orm.Trend]) \
        .where(orm.Trend.ID == int(trend_param.Value))

    trend_child = Session.execute(stmt).fetchone()

    if (trend_child == None):
        return None

    trend_child = trend_child[0]
    print(trend_child)

    return trend_child


def get_all_childs(trend: orm.Trend, trend_def_name: str, trend_param_def_name: str, __childs=None) -> List[orm.Trend]:
    if __childs is None:
        __childs = []

    child = find_child_of_trend(trend, trend_def_name, trend_param_def_name)
    if child is not None:
        __childs.append(child)
        get_all_childs(child, trend_def_name, trend_param_def_name, __childs)

    return __childs


def get_quick_trends() -> List[orm.Trend]:
    # select t.ID, t.Name
    # from lds.Trend t
    # join lds.TrendDef td on td.ID = t.TrendDefID
    # where td.Name = 'QUICK'

    stmt = sql.select([orm.Trend]) \
        .join(orm.TrendDef, orm.TrendDef.ID == orm.Trend.TrendDefID) \
        .where(orm.TrendDef.Name == 'QUICK')

    quick_trends = []
    result = Session.execute(stmt).fetchall()
    for trend in result:
        quick_trends.append(trend[0])

    return quick_trends
    #         # query = sql.select(
    #         # [orm.Method.PipelineID.label('PipelineID'),
    #         #  orm.Method.ID.label('MethodID'),
    #         #  orm.MethodParamDef.ID.label('MethodParamDefID'),
    #         #  orm.MethodParamDef.DataType.label('DataType'),
    #         #  orm.MethodParamDef.Name.label('Name'),
    #         #  orm.MethodParam.Value.label('Value')
    #         #  ]) \
    #         # .select_from(orm.Method) \
    #         # .join(orm.MethodDef, orm.Method.MethodDefID == orm.MethodDef.ID) \
    #         # .join(orm.MethodParamDef, orm.MethodDef.ID == orm.MethodParamDef.MethodDefID) \
    #         # .join(orm.MethodParam, orm.MethodParamDef.ID == orm.MethodParam.MethodParamDefID) \
    #         # .where(and_(orm.Method.PipelineID == pipeline_id, orm.MethodDef.ID == method_id))

    # pass
