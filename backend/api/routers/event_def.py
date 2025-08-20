from typing import Annotated
from fastapi import APIRouter, Body, Path, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import select, delete, Engine, literal
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse, Response
from api.routers.utils import strip_strings, get_user_token
from ..custom_page import CustomParams, CustomPage, use_custom_page
from db import get_engine
from ..schemas import api
from database import lds

router = APIRouter(prefix="/event_def", tags=["event_def"], dependencies=[Depends(get_user_token)])


@router.get('', response_model=CustomPage[lds.EventDef] | api.Error)
async def list_event_defs(engine: Annotated[Engine, Depends(get_engine)], params: Annotated[CustomParams, Depends()],
                          _: Annotated[None, Depends(use_custom_page)]):
    try:
        statement = select(lds.EventDef).order_by(lds.EventDef.ID) # noqa
        with Session(engine) as session:
            page = paginate(session, statement, params=params)
        page.items = [strip_strings(event_def) for event_def in page.items]
        return page
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_event_defs(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('', response_model=lds.EventDef | api.Error)
async def create_event_def(event_def: Annotated[api.EventDefCreate, Body()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        event_def = lds.EventDef(**event_def.model_dump())
        with Session(engine) as session:
            session.add(event_def)
            session.commit()
            session.refresh(event_def)
        content = strip_strings(event_def).model_dump(by_alias=True)
        return JSONResponse(content=content, status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        error = api.Error(code=status.HTTP_409_CONFLICT, message='Integrity error when creating event def')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_event_def(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{event_def_id}', response_model=api.Information | api.Error)
async def delete_event_def_by_id(event_def_id: Annotated[str, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            event_def = session.get(lds.EventDef, event_def_id)
            if not event_def:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No event def with id = ' + event_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            statement = delete(lds.Event).where(lds.Event.EventDefID == literal(event_def_id)) # noqa
            session.execute(statement)
            session.delete(event_def)
            session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f'Exception in delete_event_def_by_id(): {e}')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{event_def_id}', response_model=lds.EventDef | api.Error)
async def get_event_def_by_id(event_def_id: Annotated[str, Path()], engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            event_def = session.get(lds.EventDef, event_def_id)
        if not event_def:
            error = api.Error(code=status.HTTP_404_NOT_FOUND, message='No event def with id = ' + event_def_id)
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        return strip_strings(event_def)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message=f'Exception in get_event_def_by_id(): {e}')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{event_def_id}', response_model=lds.EventDef | api.Error)
async def update_event_def(event_def_id: Annotated[str, Path()], updated_event_def: Annotated[api.EventDefUpdate, Body()],
                           engine: Annotated[Engine, Depends(get_engine)]):
    try:
        with Session(engine) as session:
            event_def = session.get(lds.EventDef, event_def_id)
            if not event_def:
                error = api.Error(code=status.HTTP_404_NOT_FOUND,
                              message='No event def with id = ' + event_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_event_def_dict = updated_event_def.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_event_def_dict.items():
                setattr(event_def, k, v)
            session.commit()
            session.refresh(event_def)
        return strip_strings(event_def)
    except Exception as e:
        error = api.Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in update_event_def(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
