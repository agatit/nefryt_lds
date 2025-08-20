from typing import Annotated
from fastapi import APIRouter, Depends, Path
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, Engine
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from api.routers.utils import get_user_token
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/trend_writer", tags=["trend_writer"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[api.ProfilerData] | api.Error)
async def list_profiler_data(engine: Annotated[Engine, Depends(get_engine)],
                                          params: Annotated[CustomParams, Depends()],
                                          _: Annotated[None, Depends(use_custom_page)]):
    try:
        statement = select(lds.ProfilerData).order_by(lds.ProfilerData.ID)  # noqa
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_profiler_data(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/general', response_model=api.ProfilerGeneralData | api.Error)
async def get_general_profiler_data(engine: Annotated[Engine, Depends(get_engine)]):
    try:
        statement = select(lds.ProfilerData).order_by(lds.ProfilerData.ID)
        with Session(engine) as session:
            profiler_datas = session.execute(statement).all()
        general_data = api.ProfilerGeneralData()
        if len(profiler_datas) == 0:
            error = api.Error(code=status.HTTP_400_BAD_REQUEST, message='No stored profiler data to calculate general data')
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)
        for profiler_data in profiler_datas:
            profiler_data = profiler_data[0]
            if (profiler_data.Time10 is not None and profiler_data.Time100 is not None
                    and profiler_data.Time1000 is not None):
                general_data.Time10 += float(profiler_data.Time10)
                general_data.Time100 += float(profiler_data.Time100)
                general_data.Time1000 += float(profiler_data.Time1000)
                general_data.ActiveTrends += 1
                general_data.QueueSize += profiler_data.QueueSize if profiler_data.QueueSize else 0

        general_data.Time10 /= general_data.ActiveTrends
        general_data.Time100 /= general_data.ActiveTrends
        general_data.Time1000 /= general_data.ActiveTrends
        general_data.QueueSize /= general_data.ActiveTrends

        return general_data
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_general_profiler_data(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{trend_id}', response_model=api.ProfilerData | api.Error)
async def get_profiler_data_by_id(trend_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            profiler_data = session.get(lds.ProfilerData, trend_id)
        if not profiler_data:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No profiler data for trend with id = ' + str(trend_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return profiler_data
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_profiler_data_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
