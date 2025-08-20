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
from ..schemas import api
from database import lds

router = APIRouter(prefix="/template", tags=["template"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.Template] | api.Error)
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
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_templates(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.Template | api.Error)
async def create_template(template: Annotated[api.TemplateCreate, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        incorrect_trend_ids = validate_axes_trend_ids(template.Axes, engine)
        if len(incorrect_trend_ids) > 0:
            error = api.Error(code=status.HTTP_406_NOT_ACCEPTABLE,
                          message='No trends with ids = ' + str(incorrect_trend_ids))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_406_NOT_ACCEPTABLE)
        incorrect_unit_ids = validate_axes_unit_ids(template.Axes, engine)
        if len(incorrect_unit_ids) > 0:
            error = api.Error(code=status.HTTP_406_NOT_ACCEPTABLE,
                          message='No units with ids = ' + str(incorrect_unit_ids).replace('\'', ''))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_406_NOT_ACCEPTABLE)
        template = lds.Template(**template.model_dump())
        with Session(engine) as session:
            session.add(template)
            session.commit()
            session.refresh(template)
        content = template.model_dump(by_alias=True)
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating template')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_template(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{template_id}', response_model=None | api.Error)
async def delete_template_by_id(template_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            template = session.get(lds.Template, template_id)
            if not template:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No template with id = ' + str(template_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            session.delete(template)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in delete_template_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{template_id}', response_model=lds.Template | api.Error)
async def get_template_by_id(template_id: Annotated[int, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            template = session.get(lds.Template, template_id)
        if not template:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No template with id = ' + str(template_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return template
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                      message='Exception in get_template_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{template_id}', response_model=lds.Template | api.Error)
async def update_template(template_id: Annotated[int, Path()], updated_template: Annotated[api.TemplateUpdate, Body()],
                          engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            template = session.get(lds.Template, template_id)
            if not template:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No template with id = ' + str(template_id))
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            if updated_template.Axes is not None:
                incorrect_trend_ids = validate_axes_trend_ids(updated_template.Axes, engine)
                if len(incorrect_trend_ids) > 0:
                    error = api.Error(code=status.HTTP_406_NOT_ACCEPTABLE,
                                  message='No trends with ids = ' + str(incorrect_trend_ids))
                    return JSONResponse(content=error.model_dump(), status_code=status.HTTP_406_NOT_ACCEPTABLE)
                incorrect_unit_ids = validate_axes_unit_ids(updated_template.Axes, engine)
                if len(incorrect_unit_ids) > 0:
                    error = api.Error(code=status.HTTP_406_NOT_ACCEPTABLE,
                                  message='No units with ids = ' + str(incorrect_unit_ids).replace('\'', ''))
                    return JSONResponse(content=error.model_dump(), status_code=status.HTTP_406_NOT_ACCEPTABLE)
            updated_template_dict = updated_template.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_template_dict.items():
                setattr(template, k, v)
            session.commit()
            session.refresh(template)
        return template
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating template with id = ' + str(template_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_template(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def validate_axes_trend_ids(axes: list, engine: Engine):
    trend_ids = []
    for axis in axes:
        trend_ids = trend_ids + axis.TrendsID
    trend_ids = list(set(trend_ids))
    statement = select(lds.Trend.ID).where(lds.Trend.ID.in_(trend_ids))  # noqa
    with Session(engine) as session:
        existing_trend_ids = session.execute(statement).all()
    existing_trend_ids = [id_[0] for id_ in existing_trend_ids]
    return list(set(trend_ids) - set(existing_trend_ids))


def validate_axes_unit_ids(axes: list, engine: Engine):
    unit_ids = []
    for axis in axes:
        unit_ids = unit_ids + [axis.UnitID]
    unit_ids = list(set(unit_ids))
    statement = select(lds.Unit.ID).where(lds.Unit.ID.in_(unit_ids))  # noqa
    with Session(engine) as session:
        existing_unit_ids = session.execute(statement).all()
    existing_unit_ids = [id_[0].strip() for id_ in existing_unit_ids]
    return list(set(unit_ids) - set(existing_unit_ids))
