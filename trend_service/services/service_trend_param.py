from typing import List

import sqlalchemy as sql

from ..database import Session, engine, orm
import trend_service.services.service_trend_param_def as service_trend_param_def

__list = []


def __fetch() -> List[orm.TrendParam]:
    stmt = sql.select([orm.TrendParam])
    # print(stmt)
    result = Session.execute(stmt).fetchall()
    for trend_param in result:
        __list.append(trend_param[0])

    return get_all()


def get_all() -> List[orm.TrendParam]:
    if( __list == []):
        return __fetch()
    
    return __list

def get_TrendParam(trend_param_def: orm.TrendParamDef, trend: orm.Trend) -> orm.TrendParam:
    for trend_param in get_all():
        if trend_param.TrendParamDefID == trend_param_def.ID and trend_param.TrendID == trend.ID:
            return trend_param
    return None


def get_TrendParam_for_specific_trend(trend: orm.Trend, trend_param_name: str) -> List[orm.TrendParam]:

    trend_params = []
    trend_param_defs = service_trend_param_def.get_all_TrendParamDef_where_name_is(trend_param_name)
    
    for trend_param_def in trend_param_defs:
        for trend_param in __list:
            if (trend_param_def.ID == trend_param.TrendParamDefID) and (trend.ID == trend_param.TrendID):
                trend_params.append(trend_param)
            
    return trend_params;

def find_all_modbus_register_for_trends(trends: List[orm.Trend]) -> List[int]:
    
    __list_of_modubus_register = []
    
    trend_params = []
    
    for trend in trends:
        trend_params = get_TrendParam_for_specific_trend(trend, "ModbusRegister")
        
        for trend_param in trend_params:
            __list_of_modubus_register.append(trend_param.Value)
            
    
    return list(map(int, __list_of_modubus_register));