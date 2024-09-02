from typing import Annotated

from fastapi import APIRouter, Body, Path
from pyodbc import IntegrityError
from sqlalchemy import select, delete
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from ..db import engine
from ..routers.mapper import map_lds_trend_def_to_trend_def, map_trend_def_to_lds_trend_def
from ..schemas import TrendDef, Error, Information, UpdateTrendDef

router = APIRouter(prefix="/trend_def")


@router.get('/', response_model=list[TrendDef] | Error)
async def list_trend_defs():
    try:
        statement = select(lds.TrendDef)
        with Session(engine) as session:
            trend_defs = session.execute(statement).all()
        trend_defs_out = [map_lds_trend_def_to_trend_def(lds_trend_def) for lds_trend_def in trend_defs]
        return trend_defs_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trend_defs(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/', response_model=TrendDef | Error)
async def create_trend_def(trend_def: Annotated[TrendDef, Body()]):
    try:
        lds_trend_def = map_trend_def_to_lds_trend_def(trend_def)
        with Session(engine) as session:
            session.add(lds_trend_def)
            session.commit()
            session.refresh(lds_trend_def)
        trend_def = map_lds_trend_def_to_trend_def(lds_trend_def)
        return trend_def
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Trend def with id = ' + trend_def.id + ' already exists')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_trend_def(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{trend_def_id}', response_model=Information | Error)
async def delete_trend_def_by_id(trend_def_id: Annotated[str, Path()]):
    try:
        with Session(engine) as session:
            trend_def = session.get(lds.TrendDef, trend_def_id)
            if not trend_def:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No trend def with id = ' + trend_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(trend_def)
            session.commit()
        information = Information(message="Trend def deleted", affected=1, status=status.HTTP_204_NO_CONTENT)
        return JSONResponse(content=information.model_dump(), status_code=status.HTTP_200_OK)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_trend_def_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{trend_def_id}', response_model=TrendDef | Error)
async def update_trend_def(trend_def_id: Annotated[str, Path()], updated_trend_def: Annotated[UpdateTrendDef, Body()]):
    try:
        with Session(engine) as session:
            trend_def = session.get(lds.TrendDef, trend_def_id)
            if not trend_def:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No event def with id = ' + trend_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_trend_def_dict = updated_trend_def.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_trend_def_dict.items():
                setattr(trend_def, k, v)
            session.commit()
            session.refresh(trend_def)
        return trend_def
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_trend_def(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
