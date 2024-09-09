from datetime import datetime
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import JSONResponse
from .mapper import map_lds_event_and_lds_event_def_to_event
from ..schemas import Error, Event, Information
from ..db import engine
from ..routers.security import get_user_permissions
from database import lds

router = APIRouter(prefix="/event")


@router.get('', response_model=list[Event] | Error)
async def list_events():
    try:
        statement = (select(lds.Event, lds.EventDef)
                     .join(lds.EventDef)
                     .filter(lds.EventDef.Enabled)
                     .filter(lds.EventDef.Visible))
        with Session(engine) as session:
            events = session.execute(statement).all()
        events_out = [map_lds_event_and_lds_event_def_to_event(lds_event, lds_event_def)
                      for lds_event, lds_event_def in events]
        return events_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_events(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/{event_id}', response_model=Event | Error)
async def get_event_by_id(event_id: int):
    try:
        statement = (select(lds.Event, lds.EventDef)
                     .join(lds.EventDef)
                     .where(lds.Event.ID == event_id))
        with Session(engine) as session:
            results = session.execute(statement).all()
        if not results:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No event with id = ' + str(event_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_event, lds_event_def = results[0]
        event_out = map_lds_event_and_lds_event_def_to_event(lds_event, lds_event_def)
        return event_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_event_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/{event_id}/ack', response_model=Information | Error)
async def ack_event(event_id: int, permissions: Annotated[list[str], Depends(get_user_permissions)]):
    if 'admin' not in permissions:
        error = Error(code=status.HTTP_403_FORBIDDEN, message='Forbidden')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_403_FORBIDDEN)
    try:
        with Session(engine) as session:
            event = session.get(lds.Event, event_id)
            if not event:
                raise NoResultFound()
            event.AckDate = datetime.now()
            session.add(event)
            session.commit()
        return Information(message="Event acknowledged", affected=1, status=status.HTTP_200_OK)
    except NoResultFound:
        error = Error(code=status.HTTP_404_NOT_FOUND, message='No event with id = ' + str(event_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in ack_event(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
