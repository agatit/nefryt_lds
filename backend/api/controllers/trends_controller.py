import connexion
import struct
import itertools
import time

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.trend import Trend  # noqa: E501
from api.models.trend_data import TrendData  # noqa: E501
from api.models.trend_data_trends import TrendDataTrends  # noqa: E501
from api.models.trend_param import TrendParam  # noqa: E501
from api.models.trend_def import TrendDef  # noqa: E501
from api import util

from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import aliased
from ..db import session
from database.models import lds
from .security_controller import check_permissions


def create_trend(trend=None):  # noqa: E501
    """Create trend

    Create a trend # noqa: E501

    :param trend: 
    :type trend: dict | bytes

    :rtype: Information
    """

    if connexion.request.is_json:
        api_trend = Trend.from_dict(connexion.request.get_json())  # noqa: E501
    try:
        if connexion.request.is_json:
            trend = Trend.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_trend = lds.Trend()

        db_trend.Name = api_trend.name
        db_trend.TrendGroupID = api_trend.trend_group_id
        db_trend.TrendDefID = api_trend.trend_def_id
        db_trend.TimeExponent = api_trend.time_exponent
        db_trend.UnitID = api_trend.unit 
        db_trend.NodeID = api_trend.node_id     
        session.add(db_trend)
        
        session.commit()

        return get_trend_by_id(db_trend.ID)

    except Exception as e:
        error: Error = Error(message=str(e), code=500)
        return error, 500   


def delete_trend_by_id(trend_id, token_info={}):  # noqa: E501
    """Deletes trend

    Deletes specific trend # noqa: E501

    :param trend_id: The id of the trend to retrieve
    :type trend_id: int

    :rtype: Information
    """
    try:     
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        db_trend = session.get(lds.Trend, trend_id)
        if db_trend is None:
            return Error(message="Not Found", code=404), 404
        session.delete(db_trend)
        session.commit()

        return Information(message="Success", status=200), 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_trend_by_id(trend_id):  # noqa: E501
    """Detail trend

    Info for specific trend # noqa: E501

    :param trend_id: The id of the trend to retrieve
    :type trend_id: int

    :rtype: Trend
    """
    try:
        db_trend = session.get(lds.Trend, trend_id)
        if db_trend is None:
            return Error(message="Not Found", code=404), 404

        api_trend = Trend()
        api_trend.id = db_trend.ID
        api_trend.name = db_trend.Name
        api_trend.trend_group_id = db_trend.TrendGroupID
        api_trend.trend_def_id = db_trend.TrendDefID.strip()
        api_trend.time_exponent = db_trend.TimeExponent
        api_trend.unit = db_trend.UnitID.strip()
        api_trend.node_id = db_trend.NodeID
        api_trend.symbol = db_trend.Symbol
        api_trend.unit = db_trend.Unit_.Symbol
        api_trend.color = db_trend.Color        
        return api_trend, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def update_trend(trend_id, trend=None, token_info = {}):  # noqa: E501
    """Update trend

    Update a trend # noqa: E501

    :param trend: 
    :type trend: dict | bytes

    :rtype: Information
    """
    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_trend = Trend.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_trend = session.get(lds.Trend, trend_id)
        if db_trend is None:
            return Error(message="Not Found", code=404), 404

        db_trend.Name = api_trend.name
        db_trend.TrendGroupID = api_trend.trend_group_id
        db_trend.TrendDefID = api_trend.trend_def_id
        db_trend.TimeExponent = api_trend.time_exponent
        db_trend.UnitID = api_trend.unit
        db_trend.NodeID = api_trend.node_id 
        db_trend.Symbol = api_trend.symbol
        db_trend.Color = api_trend.color
        session.add(db_trend)

        session.commit()

        return get_trend_by_id(db_trend.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  


def list_trends(filter_=None, filter=None):  # noqa: E501
    """List trends

    List all trends # noqa: E501

    :param filter: Query filter in OData standard
    :type filter: str

    :rtype: List[Trend]
    """
    try:
        stmt = select(lds.Trend)
        if filter_ is not None:
            stmt = apply_odata_query(stmt, filter_)
        db_trends = session.execute(stmt)

        api_trends = []
        for db_trend, in db_trends:
            api_trend = Trend()
            api_trend.id = db_trend.ID
            api_trend.name = db_trend.Name
            api_trend.symbol = db_trend.Symbol
            api_trend.trend_group_id = db_trend.TrendGroupID
            api_trend.trend_def_id = db_trend.TrendDefID.strip()
            api_trend.time_exponent = db_trend.TimeExponent
            api_trend.unit = db_trend.Unit_.Symbol
            api_trend.color = db_trend.Color
            api_trend.node_id = db_trend.NodeID
            api_trends.append(api_trend)        

        return api_trends, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_trend_data(trend_id_list, begin, end, samples):  # noqa: E501
    """List trend data

    List data # noqa: E501

    :param trend_id: The id of the trend to retrieve
    :type trend_id: int
    :param begin: start of date to take from data (timestamp UTC)
    :type begin: int
    :param end: end of date to take from data (timestamp UTC)
    :type end: int
    :param samples: amount of data to take (resolution)
    :type samples: int

    :rtype: List[TrendData]
    """
    try:                           

        # reading trends defnitions neccessary for scaling
        db_trends = session.execute(select(lds.Trend))
        
        db_trends_scales = {}
        for db_trend, in db_trends:
            params = list_trend_params(db_trend.ID)
            db_trends_scales[db_trend.ID] = {
                "RawMin": next(x for x in params if x.Name == "RAW_MIN").Value,
                "RawMax":  next(x for x in params if x.Name == "RAW_MAX").Value,
                "ScaledMin": next(x for x in params if x.Name == "SCALED_MIN").Value,
                "ScaledMax": next(x for x in params if x.Name == "SCALED_MAX").Value,
                }

        # readin the trend data
        api_data_list = []

        if samples <= 0:
            samples = 1        
        inc_samples = (100 * (end - begin + 1)) // samples
        if inc_samples == 0:
            inc_samples = 1
        samples = 100 * (end - begin + 1) // inc_samples

        # preparing result list
        last_timestamp = begin
        last_timestamp_samples = 0
        for _ in range(samples):
            api_data_list.append({"Timestamp": last_timestamp, "TimestampMs": last_timestamp_samples * 10})
            last_timestamp += (last_timestamp_samples + inc_samples) // 100
            last_timestamp_samples = (last_timestamp_samples + inc_samples) % 100

        
        chunk_size = 500 # how many trend points to fetch in one query
        chunk_start = 0
    
        # for every chunk
        while chunk_start < len(api_data_list):

            timestamp_list = set()
            for data in itertools.islice(api_data_list, chunk_start, chunk_start + chunk_size):
                timestamp_list.add(data["Timestamp"])        

            db_iter = session.execute(
                select(lds.TrendData) \
                    .where(and_(lds.TrendData.Time.in_(timestamp_list), lds.TrendData.TrendID.in_(trend_id_list))) \
                    .order_by(lds.TrendData.Time) 
            )
            api_iter = itertools.islice(api_data_list, chunk_start, chunk_start + chunk_size)

            db_data = next(db_iter, None)
            api_data = next(api_iter, None)
                    
            while db_data and api_data:              
                while db_data[0].Time < api_data["Timestamp"]:
                    db_data = next(db_iter)

                one_second_data = {}
                while db_data and db_data[0].Time == api_data["Timestamp"]:
                    if db_trends_scales[db_data[0].TrendID]["RawMin"] >= 0:
                        one_second_data[db_data[0].TrendID] = struct.unpack("H"*100, db_data[0].Data)
                    else:
                        one_second_data[db_data[0].TrendID] = struct.unpack("h"*100, db_data[0].Data)
                    db_data = next(db_iter, None)

                current_second = api_data["Timestamp"]
                while api_data and api_data["Timestamp"] == current_second:
                    for trend_id in one_second_data.keys():
                        api_data[str(trend_id)] = \
                            (db_trends_scales[trend_id]["ScaledMax"] - db_trends_scales[trend_id]["ScaledMin"]) \
                            * (one_second_data[trend_id][-api_data["TimestampMs"]//10-1] - db_trends_scales[trend_id]["RawMin"]) \
                            / (db_trends_scales[trend_id]["RawMax"] - db_trends_scales[trend_id]["RawMin"]) \
                            + db_trends_scales[trend_id]["ScaledMin"]
                    api_data = next(api_iter, None)
                                    
            chunk_start += chunk_size

        # print("--- %s seconds ---" % (time.time() - start_time))        
        return api_data_list, 200   

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_trend_current_data(trend_id_list, period, samples):  # noqa: E501
    """List trend current data 
    """

    return get_trend_data(trend_id_list, int(time.time()) - period, int(time.time()), samples)


def get_trend_param_by_id(trend_id, trend_param_def_id):  # noqa: E501
    """Gets trend param detail

    Info for specific trend param # noqa: E501

    :param trend_id: The id of the trend to retrieve
    :type trend_id: int
    :param param_id: The id of the param to retrieve
    :type param_id: int

    :rtype: TrendParam
    """
    try:
        db_trend_param = session.get(lds.TrendParam, (trend_param_def_id, trend_id))
        if db_trend_param is None:
            return Error(message="Not Found", code=404), 404

        api_trend_param = TrendParam()
        api_trend_param.trend_id = db_trend_param.TrendID
        api_trend_param.trend_param_def_id = db_trend_param.TrendParamDefID.strip()
        api_trend_param.value = db_trend_param.Value

        return api_trend_param, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_trend_params(trend_id):  # noqa: E501
    """List trend params

    List all trend params # noqa: E501

    :param trend_id: The id of the trend to retrieve
    :type trend_id: int

    :rtype: List[TrendParam]
    """

    try:
        tp = aliased(lds.TrendParam)
        t = aliased(lds.Trend)
        tpd = aliased(lds.TrendParamDef)
        
        stmt = select(tp, t, tpd) \
            .select_from(t) \
            .outerjoin(tpd, t.TrendDefID == tpd.TrendDefID ) \
            .outerjoin(tp, and_(tpd.ID == tp.TrendParamDefID, t.ID == tp.TrendID)) \
            .where(t.ID == trend_id)

        db_trend_params = session.execute(stmt)

        api_trend_params = []
        for db_trend_param, db_trend, db_trend_param_def in db_trend_params:
            api_trend_param = TrendParam()
            api_trend_param.trend_id = db_trend.ID
            api_trend_param.trend_param_def_id = db_trend_param_def.ID.strip()            
            api_trend_param.name = db_trend_param_def.Name
            api_trend_param.data_type = db_trend_param_def.DataType.strip()
            if api_trend_param is not None:
                api_trend_param.value = db_trend_param.Value
            api_trend_params.append(api_trend_param)

        return api_trend_params, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def update_trend_param(trend_id, trend_param_def_id, trend_param=None, token_info={}):  # noqa: E501
    """Update trend params

    Updates trend param # noqa: E501

    :param trend_id: The id of the trend to retrieve
    :type trend_id: int
    :param trend_param: 
    :type trend_param: dict | bytes

    :rtype: Information
    """
    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403
            
        if connexion.request.is_json:
            api_trend_param = TrendParam.from_dict(connexion.request.get_json())  # noqa: E501

        db_trend_param = session.get(lds.TrendParam, (trend_param_def_id, trend_id))
        if db_trend_param is None:
            return Error(message="Not Found", code=404), 404

        
        db_trend_param.Value = api_trend_param.value
        session.add(db_trend_param)

        session.commit()

        return get_trend_param_by_id(db_trend_param.TrendID, db_trend_param.TrendParamDefID)

    except Exception as e:
        return Error(message=str(e), code=500), 500          


def list_trend_defs(filter=None, filter_=None):  # noqa: E501
    """List trends

    List all trends # noqa: E501


    :rtype: List[Trend]
    """
    try:
        stmt = select(lds.TrendDef)
        if filter_ is not None:
            stmt = apply_odata_query(stmt, filter_)

        trends = session.execute(stmt)

        api_trends = []
        for trend, in trends:
            api_trend = TrendDef()
            api_trend.id = trend.ID.strip()
            api_trend.name = trend.Name
            api_trends.append(api_trend)        

        return api_trends, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500    
