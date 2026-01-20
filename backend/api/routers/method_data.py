from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy import select, Engine, literal
from database import lds
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from api.routers.utils import get_user_token
from ..custom_page import CustomParams, use_custom_page, CustomPage
from db import get_engine
from ..schemas import base, api


router = APIRouter(prefix="/method", tags=["method_data"], dependencies=[Depends(get_user_token)])


@router.get('/{method_id}/data', response_model=CustomPage[base.MethodData] | api.Error)
async def get_method_data(method_id: Annotated[int, Path()],
                          engine: Annotated[Engine, Depends(get_engine)],
                          params: Annotated[CustomParams, Depends()],
                          _: Annotated[None, Depends(use_custom_page)]):
    try:
        with Session(engine) as session:
            lds_method = session.get(lds.Method, method_id)
        if not lds_method:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method with id = ' + str(method_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)

        statement = (select(lds.MethodData)
                     .where(lds.MethodData.MethodID == literal(method_id))  # noqa
                     .order_by(lds.MethodData.Position, lds.MethodData.Time))

        with Session(engine) as session:
            lds_method_data_rows = session.execute(statement).all()
        lds_method_data: list[lds.MethodData] = [data[0] for data in lds_method_data_rows]

        if len(lds_method_data) == 0:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No method data for method with id = ' + str(method_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        page_items = lds_method_data[(params.page-1)*params.size:params.page*params.size] if params.page*params.size < len(lds_method_data) else lds_method_data[(params.page-1)*params.size:]
        return CustomPage(items=page_items, total=len(lds_method_data),
                          pages=len(lds_method_data) // params.size if len(lds_method_data) // params.size > 1 else 1,
                          page=params.page, size=params.size)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                          message='Exception in get_method_data(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
