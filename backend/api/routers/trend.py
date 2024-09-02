import traceback
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Query, Body, Path
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from .mapper import map_lds_trend_to_trend, map_trend_to_lds_trend, \
    map_lds_trend_param_and_lds_trend_param_def_to_trend_param
from ..db import engine
from ..schemas import Error, TrendData, Information, Trend, UpdateTrend, TrendParam
from database import lds

router = APIRouter(prefix="/trend")


@router.get('/', response_model=list[Trend] | Error)
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


@router.post('/', response_model=Trend | Error)
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
        print(traceback.print_exc())
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/trend/{trend_id_list}/current_data/{period}/{samples}', response_model=list[TrendData] | Error)
async def get_trend_current_data(trend_id_list: Annotated[list[int], Path()], period: Annotated[int, Path()], samples: Annotated[int, Path()]):
    timestamp = int(datetime.now(timezone.utc).timestamp())
    return get_trend_data(trend_id_list, timestamp - period, timestamp, samples)


# todo: !!!
@router.get('/{trend_id_list}/data/{begin}/{end}/{samples}', response_model=list[TrendData] | Error)
async def get_trend_data(trend_id_list: Annotated[list[int], Path()], begin: Annotated[int, Path()], end: Annotated[int, Path()], samples: Annotated[int, Path()]):
    try:
        statement = select(lds.Trend).where(lds.Trend.ID.in_(trend_id_list))
        with Session(engine) as session:
            trends = session.execute(statement).all()
        return []
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_data(): ' + str(e))
        print(traceback.print_exc())
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
        information = Information(message="Trend deleted", affected=1, status=status.HTTP_204_NO_CONTENT)
        return JSONResponse(content=information.model_dump(), status_code=status.HTTP_200_OK)
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


@router.get('/trend/{trend_id}/param', response_model=list[TrendParam] | Error)
async def list_trend_params(trend_id: Annotated[int, Path()], filter: Annotated[str | None, Query()] = None):
    try:
        statement = (select(lds.TrendParam, lds.TrendParamDef)
                     .join(lds.TrendParamDef)
                     .where(lds.TrendParam.TrendID == trend_id))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No trend with id = ' + str(trend_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        trend_params_list = []
        for result in results:
            lds_trend_param, lds_trend_param_def = result[0]
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
