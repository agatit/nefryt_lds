from typing import Annotated
from fastapi import APIRouter, Body, Path
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from .mapper import to_dict
from ..db import engine
from ..schemas import Error, EventDef, Information
from database import lds

router = APIRouter(prefix="/event_defs")


@router.get('/', response_model=list[EventDef] | Error, operation_id="list_event_defs")
async def list_event_defs():
    try:
        statement = select(lds.EventDef)
        with Session(engine) as session:
            event_defs = session.execute(statement).all()
        event_defs_out = [EventDef(**to_dict(lds_event_def[0])) for lds_event_def in event_defs]
        return event_defs_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_event_defs(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/', response_model=EventDef | Error)
async def create_event_def(event_def: Annotated[EventDef, Body()]):
    try:
        lds_event_def = lds.EventDef(**event_def.model_dump(by_alias=True))
        with Session(engine) as session:
            session.add(lds_event_def)
            session.commit()
            session.refresh(lds_event_def)
        event_def = EventDef(**to_dict(lds_event_def))
        return event_def
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Event def with id = ' + event_def.id + ' already exists')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in create_event_def(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.delete('/{event_def_id}', response_model=Information | Error)
async def delete_event_def_by_id(event_def_id: Annotated[str, Path()]):
    try:
        with (Session(engine) as session):
            event_def = session.get(lds.EventDef, event_def_id)
            if not event_def:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No event def with id = ' + event_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            statement = delete(lds.Event).where(lds.Event.EventDefID == event_def_id)
            session.execute(statement)
            session.delete(event_def)
            session.commit()
        information = Information(message="Event def deleted", affected=1, status=status.HTTP_204_NO_CONTENT)
        return JSONResponse(content=information.model_dump(), status_code=status.HTTP_200_OK)
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when deleting event def with id =' + event_def_id)
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_event_def_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.put('/{event_def_id}', response_model=EventDef | Error)
async def update_event_def(event_def_id: Annotated[str, Path()], updated_event_def: Annotated[EventDef, Body()]):
    try:
        with Session(engine) as session:
            event_def = session.get(lds.EventDef, event_def_id)
            if not event_def:
                error = Error(code=status.HTTP_404_NOT_FOUND,
                              message='No event def with id = ' + event_def_id)
                return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
            updated_event_def_dict = updated_event_def.model_dump(by_alias=True, exclude_unset=True)
            for k, v in updated_event_def_dict.items():
                setattr(event_def, k, v)
            session.commit()
            session.refresh(event_def)
        return event_def
    except IntegrityError:
        error = Error(code=status.HTTP_409_CONFLICT,
                      message='Integrity error when updating event def with id =' + event_def_id)
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_409_CONFLICT)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in delete_event_def_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
