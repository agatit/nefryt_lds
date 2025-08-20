from typing import Annotated
from fastapi import APIRouter, Body, Path, Query, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import get_user_token
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api
from database import lds

router = APIRouter(prefix="/trend_group", tags=["trend_group"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.TrendGroup] | api.Error)
async def list_trend_groups(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                     _: Annotated[None, Depends(use_custom_page)],
                     odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.TrendGroup).order_by(lds.TrendGroup.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trend_groups(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.TrendGroup | api.Error)
async def create_trend_group(trend_group: Annotated[api.TrendGroupCreate, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        trend_group = lds.TrendGroup(**trend_group.model_dump())
        with Session(engine) as session:
            session.add(trend_group)
            session.commit()
            session.refresh(trend_group)
        content = trend_group.model_dump(by_alias=True)
        return JSONResponse(content=jsonable_encoder(content), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating trend group')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_trend_group(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{trend_group_id}', response_model=None | api.Error)
async def delete_trend_group_by_id(trend_group_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            trend_group = session.get(lds.TrendGroup, trend_group_id)
            if not trend_group:
                error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No trend group with id = ' + str(trend_group_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(trend_group)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when deleting trend group with id = ' + str(trend_group_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_trend_group_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_group_id}', response_model=lds.TrendGroup | api.Error)
async def get_trend_group_by_id(trend_group_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            trend_group = session.get(lds.TrendGroup, trend_group_id)
        if not trend_group:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No trend group with id = ' + str(trend_group_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return trend_group
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_trend_group_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{trend_group_id}', response_model=lds.TrendGroup | api.Error)
async def update_trend_group(trend_group_id: Annotated[int, Path()], updated_trend_group: Annotated[api.TrendGroupUpdate, Body()],
                      engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            trend_group = session.get(lds.TrendGroup, trend_group_id)
            if not trend_group:
                error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No trend group with id = ' + str(trend_group_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_trend_group_dict = updated_trend_group.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_trend_group_dict.items():
                setattr(trend_group, k, v)
            session.commit()
            session.refresh(trend_group)
        return trend_group
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating trend group with id = ' + str(trend_group_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_trend_group(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
