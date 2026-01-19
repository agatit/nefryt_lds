from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body, Path
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine
from sqlalchemy.exc import IntegrityError
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import strip_strings, get_user_token
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/method", tags=["method"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Method] | api.Error)
async def list_methods(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                           _: Annotated[None, Depends(use_custom_page)],
                           odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.Method).order_by(lds.Method.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(lds_method) for lds_method in page.items]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_methods(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Method | api.Error)
async def create_method(method: Annotated[api.MethodCreate, Body()],
                            engine: Annotated[Engine, Depends(get_engine)]):
    try:
        method = lds.Method(**method.model_dump())
        with Session(engine) as session:
            session.add(method)
            session.commit()
            session.refresh(method)
        content = strip_strings(method).model_dump(by_alias=True)
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating method')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_method(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{method_id}', response_model=None | api.Error)
async def delete_method_by_id(method_id: Annotated[int, Path()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            method = session.get(lds.Method, method_id)
            if not method:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No method with id = ' + str(method_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(method)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_method_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{method_id}', response_model=lds.Method | api.Error)
async def get_method_by_id(method_id: int, engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_method = session.get(lds.Method, method_id)
        if not lds_method:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method with id = ' + str(method_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return strip_strings(lds_method)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_method_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{method_id}', response_model=lds.Method | api.Error)
async def update_method(method_id: Annotated[int, Path()],
                            updated_method: Annotated[api.MethodUpdate, Body()],
                            engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            method = session.get(lds.Method, method_id)
            if not method:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No method with id = ' + str(method_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_method_dict = updated_method.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_method_dict.items():
                setattr(method, k, v)
            session.commit()
            session.refresh(method)
        return strip_strings(method)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating method with id = ' + str(method_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_method(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
