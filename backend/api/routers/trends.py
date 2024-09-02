import traceback
from typing import Annotated
from fastapi import APIRouter, Query, Body
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from .mapper import map_lds_trend_to_trend, map_trend_to_lds_trend
from ..db import engine
from ..schemas import Error
from ..schemas.trend import Trend
from database import lds

router = APIRouter(prefix="/trend")


@router.get('/', response_model=list[Trend] | Error)
async def list_trends(filter: Annotated[str | None, Query()] = None):
    try:
        statement = select(lds.Trend)
        with Session(engine) as session:
            trends = session.execute(statement).all()
        trends_out = [map_lds_trend_to_trend(lds_trend[0]) for lds_trend in trends]
        return trends_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_trends(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/', response_model=Trend | Error)
async def create_trend(trend: Annotated[Trend, Body()]):
    try:
        lds_trend = map_trend_to_lds_trend(trend)
        with Session(engine) as session:
            session.add(lds_trend)
            session.commit()
            session.refresh(lds_trend)
        trend = map_lds_trend_to_trend(lds_trend)
        return JSONResponse(content=trend.model_dump(), status_code=status.HTTP_201_CREATED)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_trend(): ' + str(e))
        print(traceback.print_exc())
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
