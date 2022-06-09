import connexion
import six
import numpy as np
import struct

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.trend import Trend  # noqa: E501
from api.models.trend_data import TrendData  # noqa: E501
from api.models.trend_data_trends import TrendDataTrends  # noqa: E501
from api.models.trend_param import TrendParam  # noqa: E501
from api.models.trend_def import TrendDef  # noqa: E501
from api import util

from sqlalchemy import alias, select, delete, and_
from api import session
from database.models import lds


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
        db_trend.UnitID = api_trend.unit_id
        session.add(db_trend)
        
        session.commit()

        return get_trend_by_id(db_trend.ID)

    except Exception as e:
        error: Error = Error(message=str(e), code=500)
        return error, 500   


def delete_trend_by_id(trend_id):  # noqa: E501
    """Deletes trend

    Deletes specific trend # noqa: E501

    :param trend_id: The id of the trend to retrieve
    :type trend_id: int

    :rtype: Information
    """
    try:        
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
        api_trend.unit_id = db_trend.UnitID.strip()

        return api_trend, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def update_trend(trend_id, trend=None):  # noqa: E501
    """Update trend

    Update a trend # noqa: E501

    :param trend: 
    :type trend: dict | bytes

    :rtype: Information
    """
    try:
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
        db_trend.UnitID = api_trend.unit_id
        session.add(db_trend)

        session.commit()

        return get_trend_by_id(db_trend.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  


def list_trends():  # noqa: E501
    """List trends

    List all trends # noqa: E501


    :rtype: List[Trend]
    """
    try:
        db_trends = session.execute(
            select(lds.Trend)
        ).fetchall()

        if db_trends is None:
            return Error(message="Not Found", code=404), 404

        api_trends = []
        for db_trend, in db_trends:
            api_trend = Trend()
            api_trend.id = db_trend.ID
            api_trend.name = db_trend.Name
            api_trend.trend_group_id = db_trend.TrendGroupID
            api_trend.trend_def_id = db_trend.TrendDefID
            api_trend.time_exponent = db_trend.TimeExponent
            api_trend.unit_id = db_trend.UnitID
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
        if samples <= 0:
            samples = 1        
        api_trend_data = []
        inc_ms = (100 * (end - begin + 1)) // samples
        if inc_ms == 0:
            inc_ms = 1
        samples = 100 * (end - begin + 1) // inc_ms

        last_timestamp = begin
        last_timestamp_ms = 0
        for _ in range(samples):
            api_trend_data.append({"timestamp": last_timestamp, "timestamp_ms": last_timestamp_ms})
            last_timestamp += (last_timestamp_ms + inc_ms) // 100
            last_timestamp_ms = (last_timestamp_ms + inc_ms) % 100

        for trend_id in trend_id_list:
            cursor = session.execute(
                select(lds.TrendData)\
                    .where(and_(lds.TrendData.Time >= begin, lds.TrendData.Time <= end, lds.TrendData.TrendID==trend_id))
            )

            db_data = cursor.fetchone()
            if db_data is not None:
                db_data_values = struct.unpack("H"*100, db_data[0].Data)
                for api_data in api_trend_data:
                    while db_data is not None and db_data[0].Time < api_data["timestamp"]:
                        db_data = cursor.fetchone()
                    if db_data is None:
                        break                        
                    if db_data[0].Time == api_data["timestamp"]:
                        api_data[str(trend_id)] = db_data_values[api_data["timestamp_ms"]]

        return api_trend_data, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500



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
        # select t.ID, tpd.ID, tpd.Name, tp.Value, tpd.DataType
        #    from lds.Trend t
        #    left join lds.TrendParamDef tpd on t.TrendDefID = tpd.TrendDefID
        #    left join lds.TrendParam tp on tpd.ID = tp.TrendParamDefID and t.ID = tp.TrendID
        # where
        #     t.ID = 101

        tp = alias(lds.TrendParam, "tp")
        t = alias(lds.Trend, "t")
        tpd = alias(lds.TrendParamDef, "tpd")
        
        stmt = select(t.c.ID.label("TrendID"), tpd.c.ID.label("TrendParamDefID"), tpd.c.Name, tp.c.Value, tpd.c.DataType) \
            .select_from(t) \
            .outerjoin(tpd, t.c.TrendDefID == tpd.c.TrendDefID ) \
            .outerjoin(tp, and_(tpd.c.ID == tp.c.TrendParamDefID, t.c.ID == tp.c.TrendID)) \
            .where(t.c.ID == trend_id)

        db_trend_params = session.execute(stmt).fetchall()


        if db_trend_params is None:
            return Error(message="Not Found", code=404), 404

        api_trend_params = []
        for db_trend_param in db_trend_params:
            api_trend_param = TrendParam()
            api_trend_param.trend_id = db_trend_param.TrendID
            api_trend_param.trend_param_def_id = db_trend_param.TrendParamDefID.strip()
            api_trend_param.value = db_trend_param.Value
            api_trend_param.name = db_trend_param.Name
            api_trend_param.data_type = db_trend_param.DataType.strip()
            api_trend_params.append(api_trend_param)

        return api_trend_params, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def update_trend_param(trend_id, trend_param_def_id, trend_param=None):  # noqa: E501
    """Update trend params

    Updates trend param # noqa: E501

    :param trend_id: The id of the trend to retrieve
    :type trend_id: int
    :param trend_param: 
    :type trend_param: dict | bytes

    :rtype: Information
    """
    try:
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

def list_trend_defs():  # noqa: E501
    """List trends

    List all trends # noqa: E501


    :rtype: List[Trend]
    """
    try:
        trends = session.execute(
            select(lds.TrendDef)
        ).fetchall()

        if trends is None:
            return Error(message="Not Found", code=500), 404

        api_trends = []
        for trend, in trends:
            api_trend = TrendDef()
            api_trend.id = trend.ID
            api_trend.name = trend.Name
            api_trends.append(api_trend)        

        return api_trends, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500    
