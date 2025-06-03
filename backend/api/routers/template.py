from typing import Annotated
from fastapi import APIRouter, Body, Path, Query, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import get_user_token
from ..custom_page import CustomParams, CustomPage, use_custom_page
from db import get_engine
from ..schemas import Error, TemplateBase, UpdateTemplate, Axis
from database import lds

router = APIRouter(prefix="/template", tags=["template"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Template] | Error)
async def list_templates(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                         _: Annotated[None, Depends(use_custom_page)],
                         odata_filter: Annotated[str | None, Query(alias='filter')] = None):
    try:
        statement = select(lds.Template).order_by(lds.Template.ID)
        if odata_filter is not None:
            statement = apply_odata_query(statement, odata_filter)
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [lds.Template.model_validate(template) for template in page.items]
        return page
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_templates(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Template | Error)
async def create_template(template: Annotated[TemplateBase, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        incorrect_trend_ids = validate_axes(template.Axes, engine)
        if len(incorrect_trend_ids) > 0:
            error = Error(code=status.HTTP_406_NOT_ACCEPTABLE,
                          message='No trends with ids = ' + str(incorrect_trend_ids))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_406_NOT_ACCEPTABLE)
        template = lds.Template(**template.model_dump())
        with Session(engine) as session:
            session.add(template)
            session.commit()
            session.refresh(template)
        content = template.model_dump(by_alias=True)
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating template')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_template(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{template_id}', response_model=None | Error)
async def delete_template_by_id(template_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            template = session.get(lds.Template, template_id)
            if not template:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No template with id = ' + str(template_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(template)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_template_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{template_id}', response_model=lds.Template | Error)
async def get_template_by_id(template_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            template = session.get(lds.Template, template_id)
        if not template:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No template with id = ' + str(template_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return template
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_template_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{template_id}', response_model=lds.Template | Error)
async def update_template(template_id: Annotated[int, Path()], updated_template: Annotated[UpdateTemplate, Body()],
                          engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            template = session.get(lds.Template, template_id)
            if not template:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No template with id = ' + str(template_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            if updated_template.Axes is not None:
                incorrect_trend_ids = validate_axes(updated_template.Axes, engine)
                if len(incorrect_trend_ids) > 0:
                    error = Error(code=status.HTTP_406_NOT_ACCEPTABLE,
                                  message='No trends with ids = ' + str(incorrect_trend_ids))
                    return JSONResponse(content=error.model_dump(), status_code=status.HTTP_406_NOT_ACCEPTABLE)
            updated_template_dict = updated_template.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_template_dict.items():
                setattr(template, k, v)
            session.commit()
            session.refresh(template)
        return template
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating template with id = ' + str(template_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_template(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def validate_axes(axes: list[Axis], engine: Engine):
    trend_ids = []
    for axis in axes:
        trend_ids = trend_ids + axis.TrendsID
    trend_ids = list(set(trend_ids))
    statement = select(lds.Trend.ID).where(lds.Trend.ID.in_(trend_ids))  # noqa
    with Session(engine) as session:
        existing_trend_ids = session.execute(statement).all()
    existing_trend_ids = [id_[0] for id_ in existing_trend_ids]
    return list(set(trend_ids) - set(existing_trend_ids))
