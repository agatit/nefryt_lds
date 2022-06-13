from typing import List

import sqlalchemy as sql
from sqlalchemy import and_
from trends_writer import session
from database import lds
from ..trends import QuickTrend, TrendBase, DerivTrend, MeanTrend, DiffTrend

from . import service_trend_def, service_trend_param_def

__list = []


def __fetch() -> List[lds.Trend]:
    stmt = sql.select([lds.Trend])
    result = session.execute(stmt).fetchall()
    for trend in result:
        __list.append(trend[0])

    return get_all()


def get_all() -> List[lds.Trend]:
    if(__list == []):
        return __fetch()

    return __list


def find_child_of_trend(trend: lds.Trend, trend_def_name: str, trend_param_def_name: str) -> lds.Trend:

    if trend is None:
        return None

    trend_def = service_trend_def.find_TrendDef_where(trend_def_name)

    if trend_def is None:
        return None

    if trend_def.ID != trend.TrendDefID:
        return None

    stmt = sql.select([lds.TrendParamDef]) \
        .where(and_(lds.TrendParamDef.Name == trend_param_def_name, lds.TrendParamDef.TrendDefID == trend.TrendDefID))

    # print(stmt)

    trend_param_def = session.execute(stmt).fetchone()
    # print(trend_param_def)
    if (trend_param_def == None):
        return None

    trend_param_def = trend_param_def[0]
    # print(trend_param_def)
    stmt = sql.select([lds.TrendParam]) \
        .where(and_(lds.TrendParam.TrendParamDefID == trend_param_def.ID,
                    lds.TrendParam.TrendID == trend.ID))

    trend_param = session.execute(stmt).fetchone()

    if (trend_param == None):
        return None

    # print(trend_param)

    trend_param = trend_param[0]

    stmt = sql.select([lds.Trend]) \
        .where(lds.Trend.ID == int(trend_param.Value))

    trend_child = session.execute(stmt).fetchone()

    if (trend_child == None):
        return None

    trend_child = trend_child[0]
    # print(trend_child)

    return trend_child


def get_all_childs(trend: lds.Trend, trend_def_name: str, trend_param_def_name: str, __childs=None) -> List[lds.Trend]:
    if __childs is None:
        __childs = []

    child = find_child_of_trend(trend, trend_def_name, trend_param_def_name)
    if child is not None:
        __childs.append(child)
        get_all_childs(child, trend_def_name, trend_param_def_name, __childs)

    return __childs


def get_quick_trends() -> List[QuickTrend]:
    stmt = sql.select([lds.Trend]) \
        .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID) \
        .where(lds.TrendDef.ID == 'QUICK')

    # print(stmt)

    quick_trends = []
    result = session.execute(stmt).fetchall()
    for trend in result:
        quickTrend = QuickTrend(trend[0])
        quick_trends.append(quickTrend)

    return quick_trends


def get_all_trends() -> List[TrendBase]:
    stms = sql.select([lds.Trend])

    trends = []

    result = session.execute(stms).fetchall()
    for trend in result:
        t = TrendBase(trend[0])
        trends.append(t)

    return trends


def find_and_add_childs(trend_base: TrendBase):

    stmt = sql.select([lds.Trend, lds.TrendDef]) \
        .join(lds.TrendDef, lds.TrendDef.ID == lds.Trend.TrendDefID) \
        .join(lds.TrendParam, lds.TrendParam.TrendID == lds.Trend.ID) \
        .join(lds.TrendParamDef, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID, lds.TrendDef.ID == lds.TrendParamDef.TrendDefID)) \
        .where(and_(lds.TrendParamDef.DataType == 'TREND', lds.TrendParam.Value == trend_base.trend.ID))

    # print(stmt)

    results = session.execute(stmt).fetchall()
    for result in results:
        trend = result[0]
        trend_def = result[1]

        if trend_def.ID.strip() == 'QUICK':
            quick_trend = QuickTrend(trend)
            trend_base.children.append(quick_trend)
        elif trend_def.ID.strip() == 'DERIV':
            deriv_trend = DerivTrend(trend, trend_base.trend.ID)
            trend_base.children.append(deriv_trend)
        elif trend_def.ID.strip() == 'MEAN':
            mean_trend = MeanTrend(trend, trend_base.trend.ID)
            trend_base.children.append(mean_trend)
        elif trend_def.ID.strip() == 'DIFF':
            diff_trend = DiffTrend(trend, trend_base.trend.ID)
            trend_base.children.append(diff_trend)
        else:
            print('Unknown trend def: ' + trend_def.Name)

    for child in trend_base.children:
        find_and_add_childs(child)

