from typing import Annotated
from fastapi import APIRouter, Depends, Query
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from api.routers.utils import strip_strings, get_user_token
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import api

router = APIRouter(prefix="/method_def", tags=["method_def"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.MethodDef] | api.Error)
async def list_method_defs(engine: Annotated[Engine, Depends(get_engine)],
                               params: Annotated[CustomParams, Depends()],
                               _: Annotated[None, Depends(use_custom_page)],
                               odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.MethodDef).order_by(lds.MethodDef.ID)  # noqa
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(lds_method_def) for lds_method_def in page.items]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in list_method_defs(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
