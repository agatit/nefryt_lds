from typing import List

import sqlalchemy as sql
from sqlalchemy import and_

from ..database import Session, engine, orm
from ..trends import QuickTrend, TrendBase, DerivTrend, DiffTrend, MeanTrend
from . import service_trend_def, service_trend_param_def

__list = []

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

    # print(stmt)

    trend_param_def = Session.execute(stmt).fetchone()
    # print(trend_param_def)
    if (trend_param_def == None):
        return None

    trend_param_def = trend_param_def[0]
    # print(trend_param_def)
    stmt = sql.select([orm.TrendParam]) \
        .where(and_(orm.TrendParam.TrendParamDefID == trend_param_def.ID,
                    orm.TrendParam.TrendID == trend.ID))

    trend_param = Session.execute(stmt).fetchone()

    if (trend_param == None):
        return None

    # print(trend_param)

    trend_param = trend_param[0]

    stmt = sql.select([orm.Trend]) \
        .where(orm.Trend.ID == int(trend_param.Value))

    trend_child = Session.execute(stmt).fetchone()

    if (trend_child == None):
        return None

    trend_child = trend_child[0]
    # print(trend_child)

    return trend_child


def get_all_childs(trend: orm.Trend, trend_def_name: str, trend_param_def_name: str, __childs=None) -> List[orm.Trend]:
    if __childs is None:
        __childs = []

    child = find_child_of_trend(trend, trend_def_name, trend_param_def_name)
    if child is not None:
        __childs.append(child)
        get_all_childs(child, trend_def_name, trend_param_def_name, __childs)

    return __childs


def get_quick_trends() -> List[QuickTrend]:
    stmt = sql.select([orm.Trend]) \
        .join(orm.TrendDef, orm.TrendDef.ID == orm.Trend.TrendDefID) \
        .where(orm.TrendDef.ID == 'QUICK')

    # print(stmt)

    quick_trends = []
    result = Session.execute(stmt).fetchall()
    for trend in result:
        quickTrend = QuickTrend(trend[0])
        quick_trends.append(quickTrend)

    return quick_trends


def get_all_trends() -> List[TrendBase]:
    stms = sql.select([orm.Trend])
    
    trends = []

    result = Session.execute(stms).fetchall()
    for trend in result:
        t = TrendBase(trend[0])
        trends.append(t)
        
    return trends
        

def find_and_add_childs(trend_base: TrendBase):

    stmt = sql.select([orm.Trend, orm.TrendDef]) \
        .join(orm.TrendDef, orm.TrendDef.ID == orm.Trend.TrendDefID) \
        .join(orm.TrendParam, orm.TrendParam.TrendID == orm.Trend.ID) \
        .join(orm.TrendParamDef, and_(orm.TrendParamDef.ID == orm.TrendParam.TrendParamDefID, orm.TrendDef.ID == orm.TrendParamDef.TrendDefID)) \
        .where(and_(orm.TrendParamDef.DataType == 'TREND', orm.TrendParam.Value == trend_base.trend.ID))

    # print(stmt)

    results = Session.execute(stmt).fetchall()
    for result in results:
        trend = result[0]
        trend_def = result[1]

        if trend_def.ID.strip() == 'QUICK':
            quick_trend = QuickTrend(trend)
            trend_base.children.append(quick_trend)
        elif trend_def.ID.strip() == 'DERIV':
            deriv_trend = DerivTrend(trend)
            trend_base.children.append(deriv_trend)
        elif trend_def.ID.strip() == 'MEAN':
            mean_trend = MeanTrend(trend)
            trend_base.children.append(mean_trend)
        elif trend_def.ID.strip() == 'DIFF':
            diff_trend = DiffTrend(trend, trend_base.trend.ID)
            trend_base.children.append(diff_trend)
        else:
            print('Unknown trend def: ' + trend_def.Name)

    for child in trend_base.children:
        find_and_add_childs(child)


def get_params_and_values(trend: orm.Trend):
    
    stmt = sql.select([orm.TrendParamDef, orm.TrendParam]) \
        .select_from(orm.Trend) \
        .join(orm.TrendDef, orm.Trend.TrendDefID == orm.TrendDef.ID) \
        .join(orm.TrendParamDef, orm.TrendDef.ID == orm.TrendParamDef.TrendDefID) \
        .join(orm.TrendParam, and_(orm.TrendParamDef.ID == orm.TrendParam.TrendParamDefID, orm.Trend.ID == orm.TrendParam.TrendID)) \
        .where(orm.Trend.ID == trend.ID)
    
    results = Session.execute(stmt).fetchall()

    __dict = {}
    for tpd, tp in results:
        __dict[tpd.Name] = tp.Value
    
    
    return __dict