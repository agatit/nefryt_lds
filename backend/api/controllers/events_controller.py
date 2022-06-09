from pydoc import visiblename
import connexion
import six
from datetime import datetime

from api.models.error import Error  # noqa: E501
from api.models.event import Event  # noqa: E501
from api.models.information import Information  # noqa: E501
from api import util

from sqlalchemy import alias, select, delete, and_
from api import session
from database.models import lds

def ack_event(event_id):  # noqa: E501
    """Acknowledges ack

    Acknowledges an event # noqa: E501

    :param event_id: The id of the event to retrieve
    :type event_id: int

    :rtype: Information
    """
    try:
        if connexion.request.is_json:
            api_event: Event = Event.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_event: lds.Event = session.get(lds.Event, api_event.id)
        if db_event is None:
            return Error(message="Not Found", code=404), 404       
        db_event.AckDate = datetime.timestamp(datetime.now())
        session.add(db_event)
        session.commit()

        return Information(message="events acknowledged", status=200), 200

    except Exception as e:
        return Error(message=str(e), code=500), 500 


def get_event_by_id(event_id):  # noqa: E501
    """Gets detailed event

    Info for specific event # noqa: E501

    :param event_id: The id of the event to retrieve
    :type event_id: int

    :rtype: Event
    """
    try:
        db_event: lds.Event = session.get(lds.Event, event_id)
        if db_event is None:
            return Error(message="Not Found", code=404), 404
        api_event = Event()
        api_event.id = db_event.ID
        api_event.method_id = db_event.MethodID
        api_event.event_def_id = db_event.EventDefID
        api_event.begin_date = db_event.BeginDate
        api_event.end_date = db_event.EndDate
        api_event.ack_date = db_event.AckDate
        api_event.details = db_event.Details
        api_event.position = db_event.Position

        return api_event, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_events():  # noqa: E501
    """List events

    List all events # noqa: E501


    :rtype: List[Event]
    """
    try:
        db_events: list[lds.Event] = session.execute(
            select(lds.Event)
                .join(lds.EventDef)
                .where(and_(lds.EventDef.Enabled == True, lds.EventDef.Visible == True))
        ).fetchall()  

        if db_events is None:
            return Error(message="Not Found", code=500), 404

        api_events = []
        for db_event, in db_events:
            api_event: Event = Event()
            api_event.id = db_event.ID
            api_event.method_id = db_event.MethodID
            api_event.event_def_id = db_event.EventDefID
            api_event.begin_date = db_event.BeginDate
            api_event.end_date = db_event.EndDate
            api_event.ack_date = db_event.AckDate
            api_event.details = db_event.Details
            api_event.position = db_event.Position 
            api_event.caption = db_event.EventDef.Caption
            api_event.verbosity = db_event.EventDef.Verbosity
            api_event.silient = db_event.EventDef.Silent

            api_events.append(api_event)   

        return api_events, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500
