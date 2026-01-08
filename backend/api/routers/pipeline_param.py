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
    map_lds_pipeline_param_and_lds_pipeline_param_def_to_api_pipeline_param, \
    map_pipeline_param_base_to_lds_pipeline_param
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/pipeline", tags=["pipeline_param"], dependencies=[Depends(get_user_token)])


@router.get('/{pipeline_id}/param', response_model=CustomPage[api.PipelineParam] | api.Error)
async def list_pipeline_params_by_pipeline_id(pipeline_id: Annotated[int, Path()],
                                              engine: Annotated[Engine, Depends(get_engine)],
                                              params: Annotated[CustomParams, Depends()],
                                              _: Annotated[None, Depends(use_custom_page)],
                                              odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(1).where(lds.Pipeline.ID == literal(pipeline_id))  # noqa
        with Session(engine) as session:
            pipeline_exists = session.execute(statement).first()
        if not pipeline_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No pipeline with id = ' + str(pipeline_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.PipelineParam, lds.PipelineParamDef)
                     .select_from(lds.PipelineParam)
                     .join(lds.PipelineParamDef, lds.PipelineParam.PipelineParamDefID == lds.PipelineParamDef.ID) # noqa
                     .join(lds.Pipeline, lds.Pipeline.ID == lds.PipelineParam.PipelineID)
                     .where(lds.PipelineParam.PipelineID == literal(pipeline_id))  # noqa
                     .order_by(lds.PipelineParamDef.ID))
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [
            map_lds_pipeline_param_and_lds_pipeline_param_def_to_api_pipeline_param(lds_pipeline_param, lds_pipeline_param_def, pipeline_id)
            for lds_pipeline_param, lds_pipeline_param_def in page.items
        ]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in list_pipeline_params_by_pipeline_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{pipeline_id}/param/all', response_model=CustomPage[api.PipelineParam] | api.Error)
async def list_required_pipeline_params_by_pipeline_id(pipeline_id: Annotated[int, Path()],
                                                       engine: Annotated[Engine, Depends(get_engine)],
                                                       params: Annotated[CustomParams, Depends()],
                                                       _: Annotated[None, Depends(use_custom_page)],
                                                       odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(1).where(lds.Pipeline.ID == literal(pipeline_id))  # noqa
        with Session(engine) as session:
            pipeline_exists = session.execute(statement).first()
        if not pipeline_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No pipeline with id = ' + str(pipeline_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (
            select(lds.PipelineParamDef, lds.PipelineParam)
            .select_from(lds.PipelineParamDef)
            .join(lds.PipelineParam, and_(lds.PipelineParamDef.ID == lds.PipelineParam.PipelineParamDefID,
                  lds.PipelineParam.PipelineID == pipeline_id), isouter=True) # noqa
            .order_by(lds.PipelineParamDef.ID))

        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [
            map_lds_pipeline_param_and_lds_pipeline_param_def_to_api_pipeline_param(lds_pipeline_param, lds_pipeline_param_def, pipeline_id)
            for lds_pipeline_param_def, lds_pipeline_param in page.items
        ]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in list_required_pipeline_params_by_pipeline_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{pipeline_id}/param/{pipeline_param_def_id}', response_model=api.PipelineParam | api.Error)
async def get_pipeline_param_by_id(pipeline_id: Annotated[int, Path()],
                                   pipeline_param_def_id: Annotated[str, Path()],
                                   engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(1).where(lds.Pipeline.ID == literal(pipeline_id))  # noqa
        with Session(engine) as session:
            pipeline_exists = session.execute(statement).first()
        if not pipeline_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No pipeline with id = ' + str(pipeline_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.PipelineParam, lds.PipelineParamDef)
                     .select_from(lds.PipelineParam)
                     .join(lds.PipelineParamDef, lds.PipelineParam.PipelineParamDefID == lds.PipelineParamDef.ID) # noqa
                     .join(lds.Pipeline, lds.Pipeline.ID == lds.PipelineParam.PipelineID) # noqa
                     .where(lds.PipelineParam.PipelineID == literal(pipeline_id))  # noqa
                     .where(lds.PipelineParamDef.ID == literal(pipeline_param_def_id)))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No pipeline param for pipeline with id = ' + str(pipeline_id)
                                      + ' and pipeline param def with id = ' + pipeline_param_def_id)
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_pipeline_param, lds_pipeline_param_def = results[0]
        return map_lds_pipeline_param_and_lds_pipeline_param_def_to_api_pipeline_param(lds_pipeline_param, lds_pipeline_param_def, pipeline_id)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in get_pipeline_param_by_pipeline_param_def_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{pipeline_id}/param/{pipeline_param_def_id}', response_model=api.PipelineParam | api.Error)
async def update_pipeline_param(pipeline_id: Annotated[int, Path()],
                                pipeline_param_def_id: Annotated[str, Path()],
                                updated_pipeline_param_value: Annotated[str, Body()],
                                engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(1).where(lds.Pipeline.ID == literal(pipeline_id))  # noqa
        with Session(engine) as session:
            pipeline_exists = session.execute(statement).first()
        if not pipeline_exists:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No pipeline with id = ' + str(pipeline_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.PipelineParam)
                     .where(lds.PipelineParam.PipelineParamDefID == literal(pipeline_param_def_id))  # noqa
                     .where(lds.PipelineParam.PipelineID == literal(pipeline_id)))
        with Session(engine) as session:
            lds_pipeline_param = session.execute(statement).all()
            if not lds_pipeline_param:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                                  message='No pipeline param for pipeline with id = ' + str(pipeline_id)
                                          + ' and pipeline param def with id = ' + pipeline_param_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_pipeline_param = lds_pipeline_param[0][0]
            lds_pipeline_param.Value = updated_pipeline_param_value
            session.commit()
        return await get_pipeline_param_by_id(pipeline_id, pipeline_param_def_id, engine)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when updating pipeline')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in update_pipeline_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/{pipeline_id}/param', response_model=api.PipelineParam | api.Error)
async def create_pipeline_param(pipeline_id: Annotated[int, Path()],
                                pipeline_param: Annotated[api.PipelineParamCreate, Body()],
                                engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_pipeline: lds.Pipeline | None = session.get(lds.Pipeline, pipeline_id)
            if not lds_pipeline:
                error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No pipeline with id = ' + str(pipeline_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            lds_pipeline_param_def: lds.PipelineParamDef | None = session.get(lds.PipelineParamDef, pipeline_param.PipelineParamDefID)
            if not lds_pipeline_param_def:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                                  message='No pipeline param def with id = ' + pipeline_param.PipelineParamDefID)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        lds_pipeline_param = map_pipeline_param_base_to_lds_pipeline_param(pipeline_param, lds_pipeline)
        with Session(engine) as session:
            session.add(lds_pipeline_param)
            session.commit()
            session.refresh(lds_pipeline_param)
        pipeline_param_out = (map_lds_pipeline_param_and_lds_pipeline_param_def_to_api_pipeline_param(lds_pipeline_param, lds_pipeline_param_def, pipeline_id))

        return JSONResponse(content=pipeline_param_out.model_dump(), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating pipeline param')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in create_pipeline_param(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{pipeline_id}/param/{pipeline_param_def_id}', response_model=None | api.Error)
async def delete_pipeline_param_by_id(pipeline_id: Annotated[int, Path()],
                                      pipeline_param_def_id: Annotated[str, Path()],
                                      engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_pipeline = session.get(lds.Pipeline, pipeline_id)
        if not lds_pipeline:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No pipeline with id = ' + str(pipeline_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        with Session(engine) as session:
            lds_pipeline_param = session.get(lds.PipelineParam, (pipeline_param_def_id, pipeline_id))
            if not lds_pipeline_param:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                                  message='No pipeline param for pipeline with id = ' + str(pipeline_id)
                                          + ' and pipeline param def with id = ' + pipeline_param_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(lds_pipeline_param)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in delete_pipeline_param_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
