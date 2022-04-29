import scipy

from ..database import Session, engine, orm
from . import (service_trend, service_trend_data, service_trend_def,
               service_trend_param, service_trend_param_def)


def calulcate_trend(trend: orm.Trend, function):
    trend_def = service_trend_def.find_TrendDef(trend)

    if trend_def.Name == "QUICK":
        print("calculate_trend: trend_def.Name == QUICK")
        service_trend_data.insert(trend.ID, function.values)
    elif trend_def.Name == "OBJ":
        print("calculate_trend: trend_def.Name == OBJ")
        pass
    elif trend_def.Name == "DERIV":
        print("calculate_trend: trend_def.Name == DERIV")

        trend_param_defs = service_trend_param_def.get_all_TrendParamDef_where(
            trend_def.ID)
        trend_id = None
        filter_window = None

        for trend_param_def in trend_param_defs:
            if trend_param_def.Name == 'TrendID':
                trend_param = service_trend_param.get_TrendParam(
                    trend, trend_param_def)
                trend_id = trend_param.Value
            if trend_param_def.Name == 'FilterWindow':
                trend_param = service_trend_param.get_TrendParam(
                    trend, trend_param_def)
                filter_window = trend_param.Value

        try:
            kernel = list(range(-filter_window, filter_window + 1))
            norm = 1/(filter_window * (filter_window + 1))
            data = list(map(int, scipy.signal.fftconvolve(
                function.values, kernel, mode='valid') * norm))
            # self.queue = self.queue[100:]
            service_trend_data.insert(trend_id, data)
        except Exception as e:
            print(e)

        pass
    elif trend_def.Name == "MEAN":
        print("calculate_trend: trend_def.Name == MEAN")
        trend_param_defs = service_trend_param_def.get_all_TrendParamDef_where(
            trend_def.ID)
        trend_id = None
        filter_window = None

        for trend_param_def in trend_param_defs:
            if trend_param_def.Name == 'TrendID':
                trend_param = service_trend_param.get_TrendParam(
                    trend, trend_param_def)
                trend_id = trend_param.Value
            if trend_param_def.Name == 'FilterWindow':
                trend_param = service_trend_param.get_TrendParam(
                    trend, trend_param_def)
                filter_window = trend_param.Value
                
        try:
            kernel = (2 * filter_window + 1) * [ 1/filter_window ]
            norm = 1/(filter_window*(filter_window+1))
            data = list(map(int, scipy.signal.fftconvolve(function.values, kernel, mode='valid') * norm))
            # self.queue = self.queue[100:]
            service_trend_data.insert(trend_id, data)
        except Exception as e:
            print(e)

        pass
    elif trend_def.Name == "DIFF":
        print("calculate_trend: trend_def.Name == DIFF")
        pass
    else:
        print("calculate_trend: Unknown trend type")
        raise Exception("Unknown trend type")
