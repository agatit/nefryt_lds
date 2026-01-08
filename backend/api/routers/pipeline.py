import traceback
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Body, Path
from fastapi.encoders import jsonable_encoder
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine
from sqlalchemy.exc import IntegrityError
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import get_user_token
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/pipeline", tags=["pipeline"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Pipeline] | api.Error)
async def list_pipelines(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                           _: Annotated[None, Depends(use_custom_page)],
                           odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.Pipeline).order_by(lds.Pipeline.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        return page
    except Exception as e:
        traceback.print_exc()
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_pipelines(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Pipeline | api.Error)
async def create_pipeline(pipeline: Annotated[api.PipelineCreate, Body()],
                            engine: Annotated[Engine, Depends(get_engine)]):
    try:
        pipeline = lds.Pipeline(**pipeline.model_dump())
        with Session(engine) as session:
            session.add(pipeline)
            session.commit()
            session.refresh(pipeline)

        content = pipeline.model_dump(by_alias=True)
        return JSONResponse(content=jsonable_encoder(content), status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating pipeline')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_pipeline(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{pipeline_id}', response_model=None | api.Error)
async def delete_pipeline_by_id(pipeline_id: Annotated[int, Path()],
                                  engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            pipeline = session.get(lds.Pipeline, pipeline_id)
            if not pipeline:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No pipeline with id = ' + str(pipeline_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(pipeline)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_pipeline_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{pipeline_id}', response_model=lds.Pipeline | api.Error)
async def get_pipeline_by_id(pipeline_id: int, engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            lds_pipeline = session.get(lds.Pipeline, pipeline_id)
        if not lds_pipeline:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No pipeline with id = ' + str(pipeline_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return lds_pipeline
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_pipeline_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{pipeline_id}', response_model=lds.Pipeline | api.Error)
async def update_pipeline(pipeline_id: Annotated[int, Path()],
                            updated_pipeline: Annotated[api.PipelineUpdate, Body()],
                            engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            pipeline = session.get(lds.Pipeline, pipeline_id)
            if not pipeline:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No pipeline with id = ' + str(pipeline_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_pipeline_dict = updated_pipeline.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_pipeline_dict.items():
                setattr(pipeline, k, v)
            session.commit()
            session.refresh(pipeline)
        return pipeline
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating pipeline with id = ' + str(pipeline_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_pipeline(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
