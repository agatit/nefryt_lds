from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body, Path
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine, literal, and_
from sqlalchemy.exc import IntegrityError
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import get_user_token, \
    map_lds_method_param_and_lds_method_param_def_to_api_method_param, \
    map_method_param_base_to_lds_method_param, strip_strings
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/method", tags=["method_param"], dependencies=[Depends(get_user_token)])


@router.get('/param/def', response_model=CustomPage[lds.MethodParamDef] | api.Error)
async def list_method_param_defs(engine: Annotated[Engine, Depends(get_engine)],
                                 params: Annotated[CustomParams, Depends()],
                                 _: Annotated[None, Depends(use_custom_page)],
                                 odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.MethodParamDef).order_by(lds.MethodParamDef.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(lds_method_param_def) for lds_method_param_def in page.items]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in list_method_param_defs(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{method_id}/param', response_model=CustomPage[api.MethodParam] | api.Error)
async def list_method_params_by_method_id(method_id: Annotated[int, Path()],
                                          engine: Annotated[Engine, Depends(get_engine)],
                                          params: Annotated[CustomParams, Depends()],
                                          _: Annotated[None, Depends(use_custom_page)],
                                          odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(1).where(lds.Method.ID == literal(method_id))  # noqa
        with Session(engine) as session:
            method_exists = session.execute(statement).first()
        if not method_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method with id = ' + str(method_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.MethodParam, lds.Method, lds.MethodParamDef)
                     .select_from(lds.MethodParam)
                     .join(lds.Method, lds.Method.ID == lds.MethodParam.MethodID)  # noqa
                     .join(lds.MethodParamDef,
                           and_(lds.MethodParam.MethodParamDefID == lds.MethodParamDef.ID,
                                lds.MethodParamDef.MethodDefID == lds.Method.MethodDefID))  # noqa
                     .where(lds.MethodParam.MethodID == method_id)  # noqa
                     .order_by(lds.MethodParamDef.ID))
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [
            map_lds_method_param_and_lds_method_param_def_to_api_method_param(lds_method_param, lds_method_param_def, method_id)
            for lds_method_param, _, lds_method_param_def in page.items
        ]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in list_method_params_by_method_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{method_id}/param/all', response_model=CustomPage[api.MethodParam] | api.Error)
async def list_required_method_params_by_method_id(method_id: Annotated[int, Path()],
                                                   engine: Annotated[Engine, Depends(get_engine)],
                                                   params: Annotated[CustomParams, Depends()],
                                                   _: Annotated[None, Depends(use_custom_page)],
                                                   odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(1).where(lds.Method.ID == literal(method_id))  # noqa
        with Session(engine) as session:
            method_exists = session.execute(statement).first()
        if not method_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method with id = ' + str(method_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (
            select(lds.MethodParamDef, lds.MethodParam, lds.Method)
            .join(lds.MethodParamDef, lds.Method.MethodDefID == lds.MethodParamDef.MethodDefID)  # noqa
            .join(lds.MethodParam,and_(lds.MethodParamDef.ID == lds.MethodParam.MethodParamDefID,
                                       lds.Method.ID == lds.MethodParam.MethodID), isouter=True)
            .where(lds.Method.ID == literal(method_id))
            .order_by(lds.MethodParamDef.ID))

        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [
            map_lds_method_param_and_lds_method_param_def_to_api_method_param(lds_method_param, lds_method_param_def, method_id)
            for lds_method_param_def, lds_method_param, _ in page.items
        ]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in list_required_method_params_by_method_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{method_id}/param/{method_param_def_id}', response_model=api.MethodParam | api.Error)
async def get_method_param_by_id(method_id: Annotated[int, Path()],
                                 method_param_def_id: Annotated[str, Path()],
                                 engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(1).where(lds.Method.ID == literal(method_id))  # noqa
        with Session(engine) as session:
            method_exists = session.execute(statement).first()
        if not method_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method with id = ' + str(method_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.MethodParam, lds.MethodParamDef)
                     .select_from(lds.MethodParam)
                     .join(lds.MethodParamDef, lds.MethodParam.MethodParamDefID == lds.MethodParamDef.ID) # noqa
                     .join(lds.Method, lds.Method.ID == lds.MethodParam.MethodID)
                     .where(lds.MethodParam.MethodID == literal(method_id))  # noqa
                     .where(lds.MethodParamDef.ID == literal(method_param_def_id)))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No method param for method with id = ' + str(method_id)
                                      + ' and method param def with id = ' + method_param_def_id)
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_method_param, lds_method_param_def = results[0]
        return map_lds_method_param_and_lds_method_param_def_to_api_method_param(lds_method_param, lds_method_param_def, method_id)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in get_method_param_by_method_param_def_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{method_id}/param/{method_param_def_id}', response_model=api.MethodParam | api.Error)
async def update_method_param(method_id: Annotated[int, Path()],
                              method_param_def_id: Annotated[str, Path()],
                              updated_method_param_value: Annotated[str, Body()],
                              engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(1).where(lds.Method.ID == literal(method_id))  # noqa
        with Session(engine) as session:
            method_exists = session.execute(statement).first()
        if not method_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method with id = ' + str(method_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.MethodParam)
                     .where(lds.MethodParam.MethodParamDefID == literal(method_param_def_id))  # noqa
                     .where(lds.MethodParam.MethodID == literal(method_id)))
        with Session(engine) as session:
            lds_method_param = session.execute(statement).all()
            if not lds_method_param:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                                  message='No method param for method with id = ' + str(method_id)
                                          + ' and method param def with id = ' + method_param_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_method_param = lds_method_param[0][0]
            lds_method_param.Value = updated_method_param_value
            session.commit()
        return await get_method_param_by_id(method_id, method_param_def_id, engine)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when updating method')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in update_method_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/{method_id}/param', response_model=api.MethodParam | api.Error)
async def create_method_param(method_id: Annotated[int, Path()],
                              method_param: Annotated[api.MethodParamCreate, Body()],
                              engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_method: lds.Method | None = session.get(lds.Method, method_id)
            if not lds_method:
                error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method with id = ' + str(method_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_method_param_def: lds.MethodParamDef | None = session.get(lds.MethodParamDef,
                                                                          (method_param.MethodParamDefID,
                                                                           lds_method.MethodDefID))
            if not lds_method_param_def:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                                  message='No method param def with id = ' + method_param.MethodParamDefID)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        lds_method_param = map_method_param_base_to_lds_method_param(method_param, lds_method)
        with Session(engine) as session:
            session.add(lds_method_param)
            session.commit()
            session.refresh(lds_method_param)
        method_param_out = (map_lds_method_param_and_lds_method_param_def_to_api_method_param
                            (lds_method_param, lds_method_param_def, method_id))

        return JSONResponse(content=method_param_out.model_dump(), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating method param')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in create_method_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{method_id}/param/{method_param_def_id}', response_model=None | api.Error)
async def delete_method_param_by_id(method_id: Annotated[int, Path()],
                                    method_param_def_id: Annotated[str, Path()],
                                    engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_method = session.get(lds.Method, method_id)
        if not lds_method:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method with id = ' + str(method_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        with Session(engine) as session:
            lds_method_param = session.get(lds.MethodParam, (method_param_def_id, method_id))
            if not lds_method_param:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                                  message='No method param for method with id = ' + str(method_id)
                                          + ' and method param def with id = ' + method_param_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(lds_method_param)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in delete_method_param_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
