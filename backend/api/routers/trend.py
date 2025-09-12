from typing import Annotated
from fastapi import APIRouter, Query, Body, Path, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import strip_strings, get_user_token
from ..custom_page import CustomParams, CustomPage, use_custom_page
from db import get_engine
from ..schemas import api
from database import lds

router = APIRouter(prefix="/trend", tags=['trend'], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Trend] | api.Error)
async def list_trends(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                      _: Annotated[None, Depends(use_custom_page)],
                      odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.Trend).order_by(lds.Trend.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(lds_trend) for lds_trend in page.items]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trends(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Trend | api.Error)
async def create_trend(trend: Annotated[api.TrendCreate, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        trend = lds.Trend(**trend.model_dump())
        with Session(engine) as session:
            session.add(trend)
            session.commit()
            session.refresh(trend)
        content = strip_strings(trend).model_dump(by_alias=True)
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating trend')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_trend(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{trend_id}', response_model=None | api.Error)
async def delete_trend_by_id(trend_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            trend = session.get(lds.Trend, trend_id)
            if not trend:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend with id = ' + str(trend_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(trend)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_trend_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}', response_model=lds.Trend | api.Error)
async def get_trend_by_id(trend_id: int, engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_trend = session.get(lds.Trend, trend_id)
        if not lds_trend:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No trend with id = ' + str(trend_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return strip_strings(lds_trend)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{trend_id}', response_model=lds.Trend | api.Error)
async def update_trend(trend_id: Annotated[int, Path()], updated_trend: Annotated[api.TrendUpdate, Body()],
                       engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            trend = session.get(lds.Trend, trend_id)
            if not trend:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend with id = ' + str(trend_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_trend_dict = updated_trend.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_trend_dict.items():
                setattr(trend, k, v)
            lds.Trend.model_validate(trend)
            session.commit()
            session.refresh(trend)
        return strip_strings(trend)
    except ValueError as e:
        error = api.Error(code=status.HTTP_422_UNPROCESSABLE_ENTITY, message=str(e.errors()[0]['ctx']['error']))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_trend(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{trend_id}/enable', response_model=None | api.Error)
async def enable_trend(trend_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            trend = session.get(lds.Trend, trend_id)
            if not trend:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,  message='No trend with id = ' + str(trend_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            trend.Enabled = not trend.Enabled
            lds.Trend.model_validate(trend)
            session.commit()
            session.refresh(trend)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in enable_trend(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
