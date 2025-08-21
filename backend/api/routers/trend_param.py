from typing import Annotated
from fastapi import APIRouter, Query, Body, Path, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, and_, Engine, literal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import map_lds_trend_param_and_lds_trend_param_def_to_trend_param, get_user_token
from ..custom_page import CustomParams, CustomPage, use_custom_page
from db import get_engine
from ..schemas import api
from database import lds

router = APIRouter(prefix="/trend", tags=['trend_param'], dependencies=[Depends(get_user_token)])


@router.get('/{trend_id}/param', response_model=CustomPage[api.TrendParam] | api.Error)
async def list_trend_params(trend_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)],
                            params: Annotated[CustomParams, Depends()], _: Annotated[None, Depends(use_custom_page)],
                            odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(1).where(lds.Trend.ID == literal(trend_id)) # noqa
        with Session(engine) as session:
            trend_exists = session.execute(statement).first()
        if not trend_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No trend with id = ' + str(trend_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        statement = ((((select(lds.TrendParam, lds.Trend, lds.TrendParamDef)
                        .select_from(lds.Trend))
                       .join(lds.TrendParamDef, lds.Trend.TrendDefID == lds.TrendParamDef.TrendDefID)) # noqa
                      .join(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID,
                                                 lds.Trend.ID == lds.TrendParam.TrendID))) # noqa
                     .where(lds.Trend.ID == literal(trend_id)) # noqa
                     .order_by(lds.Trend.ID)) # noqa
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [
            map_lds_trend_param_and_lds_trend_param_def_to_trend_param(lds_trend_param, lds_trend_param_def)
            for lds_trend_param, _, lds_trend_param_def in page.items
        ]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trend_params(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/{trend_id}/param', response_model=api.TrendParam | api.Error)
async def create_trend_param(trend_id: Annotated[int, Path()], trend_param: Annotated[api.TrendParamCreate, Body()],
                             engine: Annotated[Engine, Depends(get_engine)]):
    try:
        trend_param_dict = trend_param.model_dump()
        trend_param_dict.update({'TrendID': trend_id})
        trend_param = lds.TrendParam(**trend_param_dict)
        with Session(engine) as session:
            statement1 = select(lds.Trend).where(lds.Trend.ID == literal(trend_id))  # noqa
            trend = session.execute(statement1).fetchall()
            if not trend:
                error = api.Error(code=status.HTTP_409_CONFLICT, message='No trend with id = ' + str(trend_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
            trend = trend[0][0]
            statement2 = select(lds.TrendParamDef).where(
                and_(lds.TrendParamDef.ID == literal(trend_param.TrendParamDefID),
                     lds.TrendParamDef.TrendDefID == trend.TrendDefID))  # noqa
            trend_param_def = session.execute(statement2).fetchall()
            if not trend_param_def:
                error = api.Error(code=status.HTTP_409_CONFLICT, message='No TrendParamDef with id = ' + trend_param.TrendParamDefID)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
            session.add(trend_param)
            session.commit()
        response_content = await get_trend_param_by_id(trend_id, trend_param_dict['TrendParamDefID'], engine)
        return JSONResponse(content=response_content.model_dump(), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating trend param')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_trend_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{trend_id}/param/{trend_param_def_id}', response_model=api.Information | api.Error)
async def delete_trend_param_by_id(trend_id: Annotated[int, Path()], trend_param_def_id: Annotated[str, Path()],
                             engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = (select(lds.TrendParam).where(and_(lds.TrendParam.TrendID == literal(trend_id),
                                                       lds.TrendParam.TrendParamDefID == literal(trend_param_def_id))))
        with Session(engine) as session:
            trend_param_def = session.execute(statement).first()
            if not trend_param_def:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend param with id = ' + trend_param_def_id + ' for trend with id = ' + str(trend_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(trend_param_def[0])
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_trend_param_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}/param/{trend_param_def_id}', response_model=api.TrendParam | api.Error)
async def get_trend_param_by_id(trend_id: Annotated[int, Path()], trend_param_def_id: Annotated[str, Path()],
                                engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = ((((select(lds.TrendParam, lds.Trend, lds.TrendParamDef)
                        .select_from(lds.Trend))
                       .outerjoin(lds.TrendParamDef, lds.Trend.TrendDefID == lds.TrendParamDef.TrendDefID)) # noqa
                      .outerjoin(lds.TrendParam, and_(lds.TrendParamDef.ID == lds.TrendParam.TrendParamDefID,
                                                      lds.Trend.ID == lds.TrendParam.TrendID))) # noqa
                     .where(lds.Trend.ID == literal(trend_id)) # noqa
                     .where(lds.TrendParam.TrendParamDefID == literal(trend_param_def_id)))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = api.Error(code=status.HTTP_404_NOT_FOUND,
                          message='No trend param for trend with id = ' + str(trend_id)
                                  + ' and trendParamDef with id = ' + trend_param_def_id.strip())
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_trend_param, _, lds_trend_param_def = results[0]
        return map_lds_trend_param_and_lds_trend_param_def_to_trend_param(lds_trend_param, lds_trend_param_def)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_trend_param_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{trend_id}/param/{trend_param_def_id}', response_model=api.TrendParam | api.Error)
async def update_trend_param(trend_id: Annotated[int, Path()], trend_param_def_id: Annotated[str, Path()],
                             updated_trend_param_value: Annotated[str, Body()],
                             engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = (select(lds.TrendParam).
                     where(lds.TrendParam.TrendParamDefID == literal(trend_param_def_id)). # noqa
                     where(lds.TrendParam.TrendID == literal(trend_id)))
        with Session(engine) as session:
            lds_trend_param = session.execute(statement).all()
            lds_trend = session.get(lds.Trend, trend_id)
            if not lds_trend_param or not lds_trend:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend param for trend with id = ' + str(trend_id)
                                      + ' and trendParamDef with id = ' + trend_param_def_id.strip())
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_trend_param = lds_trend_param[0][0]
            lds_trend_param.Value = updated_trend_param_value
            session.commit()
        return await get_trend_param_by_id(trend_id, trend_param_def_id, engine)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in update_trend_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
