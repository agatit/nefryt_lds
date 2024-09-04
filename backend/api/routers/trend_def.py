from fastapi import APIRouter
from sqlalchemy import select
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from ..db import engine
from ..routers.mapper import map_lds_trend_def_to_trend_def
from ..schemas import TrendDef, Error

router = APIRouter(prefix="/trend_def")


@router.get('', response_model=list[TrendDef] | Error)
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
