from fastapi import APIRouter
from sqlalchemy.exc import NoResultFound
from starlette import status
from starlette.responses import JSONResponse

from ..repository import get_events_repository, get_event_by_id_repository, set_event_ack_date_repository
from ..schemas import Error, Event, Information
from database import lds

router = APIRouter(prefix="/events")


# todo: check if mapping correct


@router.get('/', response_model=list[Event] | Error)
async def list_events():
    try:
        events = get_events_repository()
        events_out = [map_lds_event_and_lds_event_def_to_event(lds_event, lds_event_def) for lds_event, lds_event_def in events]
        return events_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in list_events(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.get('/get/{event_id}', response_model=Event | Error)
async def get_event_by_id(event_id: int):
    try:
        result = get_event_by_id_repository(event_id)
        if not result:
            error = Error(code=status.HTTP_404_NOT_FOUND, message='No event with id = ' + str(event_id))
            return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
        lds_event, lds_event_def = result[0]
        event_out = map_lds_event_and_lds_event_def_to_event(lds_event, lds_event_def)
        return event_out
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in get_event_by_id(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/{event_id}/ack', response_model=Information | Error)
async def ack_event(event_id: int):
    try:
        set_event_ack_date_repository(event_id)
        return Information(message="Event acknowledged", affected=1, status=status.HTTP_200_OK)
    except NoResultFound:
        error = Error(code=status.HTTP_404_NOT_FOUND, message='No event with id = ' + str(event_id))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        error = Error(code=status.HTTP_500_INTERNAL_SERVER_ERROR, message='Exception in ack_event(): ' + str(e))
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def to_dict(o) -> dict:
    return {c.name: getattr(o, c.name) for c in o.__table__.columns}


def map_lds_event_and_lds_event_def_to_event(lds_event: lds.Event, lds_event_def: lds.EventDef) -> Event:
    lds_event_dict = to_dict(lds_event)
    lds_event_def_dict = to_dict(lds_event_def)
    lds_event_def_dict.pop('ID')
    lds_event_dict.update(lds_event_def_dict)
    return Event(**lds_event_dict)
