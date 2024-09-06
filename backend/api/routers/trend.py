import struct
import traceback
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Query, Body, Path
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from .mapper import map_lds_trend_to_trend, map_trend_to_lds_trend, \
    map_lds_trend_param_and_lds_trend_param_def_to_trend_param, map_dicts_to_trend_data
from ..db import engine
from ..schemas import Error, TrendData, Information, Trend, UpdateTrend, TrendParam
from database import lds

router = APIRouter(prefix="/trend")


@router.get('', response_model=list[Trend] | Error)
async def list_trends(filter: Annotated[str | None, Query()] = None):
    try:
        statement = select(lds.Trend)
        with Session(engine) as session:
            trends = session.execute(statement).all()
        trends_out = [map_lds_trend_to_trend(lds_trend[0]) for lds_trend in trends]
        return trends_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trends(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=Trend | Error)
async def create_trend(trend: Annotated[Trend, Body()]):
    try:
        lds_trend = map_trend_to_lds_trend(trend)
        with Session(engine) as session:
            session.add(lds_trend)
            session.commit()
            session.refresh(lds_trend)
        trend = map_lds_trend_to_trend(lds_trend)
        return JSONResponse(content=trend.model_dump(), status_code=status.HTTP_201_CREATED)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_trend(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id_list}/current_data/{period}/{samples}', response_model=list[TrendData] | Error)
async def get_trend_current_data(trend_id_list: Annotated[str, Path()], period: Annotated[int, Path()], samples: Annotated[int, Path()]):
    timestamp = int(datetime.now(timezone.utc).timestamp())
    return await get_trend_data(trend_id_list, timestamp - period, timestamp, samples)


# todo: not enough data between begin and end
@router.get('/{trend_id_list}/data/{begin}/{end}/{samples}', response_model=list[TrendData] | Error)
async def get_trend_data(trend_id_list: Annotated[str, Path()], begin: Annotated[int, Path()], end: Annotated[int, Path()], samples: Annotated[int, Path()]):
    try:
        lds_trends_scales = {}
        trend_id_list = trend_id_list.split(",")
        statement = select(lds.Trend).where(lds.Trend.ID.in_(trend_id_list))
        with Session(engine) as session:
            lds_trends = session.execute(statement).all()

        params_ids = ['RawMin', 'RawMax', 'ScaledMin', 'ScaledMax']
        default_lds_trends_scale = {params_ids[0]: 0,
                                    params_ids[1]: 1,
                                    params_ids[2]: 0,
                                    params_ids[3]: 1}

        for lds_trend, in lds_trends:
            try:
                lds_trends_scales[lds_trend.ID] = {
                    param_id:  getattr(lds_trend, param_id) for param_id in params_ids
                }
            except Exception as e: # noqa
                lds_trends_scales[lds_trend.ID] = default_lds_trends_scale

        samples = samples if samples > 0 else 1
        inc_samples = (100 * (end - begin + 1)) // samples
        inc_samples = inc_samples if inc_samples > 0 else 1
        samples = 100 * (end - begin + 1) // inc_samples

        trend_datas = []
        trend_timestamps = []
        trend_timestamps_ms = []
        timestamp = begin
        sample_in_timestamp = 0
        for _ in range(samples):
            trend_datas.append({"Timestamp": timestamp, "TimestampMs": sample_in_timestamp * 10})
            trend_timestamps.append(timestamp)
            trend_timestamps_ms.append(sample_in_timestamp * 10)
            timestamp += (sample_in_timestamp + inc_samples) // 100
            sample_in_timestamp = (sample_in_timestamp + inc_samples) % 100

        statement = (select(lds.TrendData).
                     where(lds.TrendData.Time.in_(trend_timestamps)).
                     where(lds.TrendData.TrendID.in_(trend_id_list)).
                     order_by(lds.TrendData.Time))
        with Session(engine) as session:
            lds_trends_data = session.execute(statement).all()

        lds_trends_data = [trend_data[0] for trend_data in lds_trends_data]

        if not lds_trends_data:
            error = Error(code=status.HTTP_404_NOT_FOUND,
                          message='No data')
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        iter_lds_data = iter(lds_trends_data)
        iter_time_data = iter(trend_datas)

        lds_data = next(iter_lds_data, None)
        time_data = next(iter_time_data, None)

        result_lists = {str(lds_trend[0].ID): [] for lds_trend in lds_trends}

        while lds_data and time_data:
            print(lds_data.Time)
            print(time_data["Timestamp"])
            while lds_data.Time < time_data["Timestamp"]:
                print('okkk')
                lds_data = next(iter_lds_data)

            one_second_data = {}
            while lds_data and lds_data.Time == time_data["Timestamp"]:
                if lds_trends_scales[lds_data.TrendID]["RawMin"] >= 0:
                    one_second_data[lds_data.TrendID] = struct.unpack("H" * 100, lds_data.Data)
                else:
                    one_second_data[lds_data.TrendID] = struct.unpack("h" * 100, lds_data.Data)
                print(one_second_data)
                if not one_second_data:
                    print(trend_datas)
                    print('xxxxx')
                    trend_datas.remove(time_data)
                    print(trend_datas)
                lds_data = next(iter_lds_data, None)

            current_second = time_data["Timestamp"]
            while time_data and time_data["Timestamp"] == current_second:
                for trend_id in one_second_data.keys():
                    result_lists[str(trend_id)].append(((lds_trends_scales[trend_id]["ScaledMax"]
                                                - lds_trends_scales[trend_id]["ScaledMin"])
                                                * (one_second_data[trend_id][-time_data["TimestampMs"] // 10 - 1]
                                                   - lds_trends_scales[trend_id]["RawMin"])
                                                / (lds_trends_scales[trend_id]["RawMax"]
                                                   - lds_trends_scales[trend_id]["RawMin"])
                                                + lds_trends_scales[trend_id]["ScaledMin"]))
                time_data = next(iter_time_data, None)

        return map_dicts_to_trend_data(trend_datas, result_lists)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_data(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{trend_id}', response_model=Information | Error)
async def delete_trend_by_id(trend_id: Annotated[int, Path()]):
    try:
        with Session(engine) as session:
            trend = session.get(lds.Trend, trend_id)
            if not trend:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend with id = ' + str(trend_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(trend)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_trend_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}', response_model=Trend | Error)
async def get_trend_by_id(trend_id: int):
    try:
        with Session(engine) as session:
            lds_trend = session.get(lds.Trend, trend_id)
        if not lds_trend:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No trend with id = ' + str(trend_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_trend = lds_trend[0]
        trend = map_lds_trend_to_trend(lds_trend)
        return trend
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{trend_id}', response_model=Trend | Error)
async def update_trend(trend_id: Annotated[str, Path()], updated_trend: Annotated[UpdateTrend, Body()]):
    try:
        with Session(engine) as session:
            trend = session.get(lds.Trend, trend_id)
            if not trend:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend with id = ' + trend_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_trend_dict = updated_trend.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_trend_dict.items():
                setattr(trend, k, v)
            session.commit()
            session.refresh(trend)
        return trend
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_trend_def(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}/param', response_model=list[TrendParam] | Error)
async def list_trend_params(trend_id: Annotated[int, Path()], filter: Annotated[str | None, Query()] = None):
    try:
        statement = ((((select(lds.TrendParam, lds.Trend, lds.TrendParamDef)
                     .select_from(lds.Trend))
                     .outerjoin(lds.TrendParamDef, lds.Trend.TrendDefID == lds.TrendParamDef.TrendDefID)) # noqa
                     .outerjoin(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID,
                                                     lds.Trend.ID == lds.TrendParam.TrendID)))
                     .where(lds.Trend.ID == trend_id))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No trend with id = ' + str(trend_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        trend_params_list = []
        for lds_trend_param, _, lds_trend_param_def in results:
            trend_param_out = map_lds_trend_param_and_lds_trend_param_def_to_trend_param(lds_trend_param, lds_trend_param_def)
            trend_params_list.append(trend_param_out)
        return trend_params_list
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trend_params(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/trend/{trend_id}/param/{trend_param_def_id}', response_model=TrendParam | Error)
async def get_trend_param_by_id(trend_id: Annotated[int, Path()], trend_param_def_id: Annotated[str, Path()]):
    try:
        statement = (select(lds.TrendParam, lds.TrendParamDef)
                     .join(lds.TrendParamDef)
                     .where(lds.TrendParam.TrendID == trend_id)
                     .where(lds.TrendParam.TrendParamDefID == trend_param_def_id))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = Error(code=status.HTTP_404_NOT_FOUND,
                          message='No trend param for trend with id = ' + str(trend_id)
                                  + ' and trendParamDef with id = ' + trend_param_def_id)
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_trend_param, lds_trend_param_def = results[0]
        trend_param_out = map_lds_trend_param_and_lds_trend_param_def_to_trend_param(lds_trend_param, lds_trend_param_def)
        return trend_param_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_param_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/trend/{trend_id}/param/{trend_param_def_id}', response_model=TrendParam | Error)
async def update_trend_param(trend_id: Annotated[str, Path()], trend_param_def_id: Annotated[str, Path()], updated_trend_param: Annotated[TrendParam, Body()]):
    try:
        statement = (select(lds.TrendParam, lds.TrendParamDef)
                     .join(lds.TrendParamDef)
                     .where(lds.TrendParam.TrendID == trend_id)
                     .where(lds.TrendParam.TrendParamDefID == trend_param_def_id))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = Error(code=status.HTTP_404_NOT_FOUND,
                          message='No trend param for trend with id = ' + str(trend_id)
                                  + ' and trendParamDef with id = ' + trend_param_def_id)
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        new_value = updated_trend_param.model_dump(by_alias=True)['Value']
        lds_trend_param = results[0]
        lds_trend_param.value = new_value
        session.commit()
        session.refresh(lds_trend_param)
        return lds_trend_param
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_trend_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
