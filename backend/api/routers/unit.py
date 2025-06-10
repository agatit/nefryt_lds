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
from api.routers.utils import get_user_token, strip_strings
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import Error, UpdateUnit, UnitBase
from database import lds

router = APIRouter(prefix="/unit", tags=["unit"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Unit] | Error)
async def list_units(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                     _: Annotated[None, Depends(use_custom_page)],
                     odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.Unit).order_by(lds.Unit.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        return page
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_units(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Unit | Error)
async def create_unit(unit: Annotated[UnitBase, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        unit = lds.Unit(**unit.model_dump())
        with Session(engine) as session:
            session.add(unit)
            session.commit()
            session.refresh(unit)
        content = strip_strings(unit).model_dump(by_alias=True)
        return JSONResponse(content=jsonable_encoder(content), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating unit')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_unit(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{unit_id}', response_model=None | Error)
async def delete_unit_by_id(unit_id: Annotated[str, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            unit = session.get(lds.Unit, unit_id)
            if not unit:
                error = Error(code=status.HTTP_404_NOT_FOUND, message='No unit with id = ' + unit_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(unit)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_unit_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{unit_id}', response_model=lds.Unit | Error)
async def get_unit_by_id(unit_id: Annotated[str, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            unit = session.get(lds.Unit, unit_id)
        if not unit:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No unit with id = ' + unit_id)
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return strip_strings(unit)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_unit_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{unit_id}', response_model=lds.Unit | Error)
async def update_unit(unit_id: Annotated[str, Path()], updated_unit: Annotated[UpdateUnit, Body()],
                      engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            unit = session.get(lds.Unit, unit_id)
            if not unit:
                error = Error(code=status.HTTP_404_NOT_FOUND, message='No unit with id = ' + unit_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_unit_dict = updated_unit.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_unit_dict.items():
                setattr(unit, k, v)
            session.commit()
            session.refresh(unit)
        return strip_strings(unit)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating unit with id = ' + unit_id)
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_unit(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
