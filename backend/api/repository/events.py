from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from ..db import engine
from database import lds


def get_events_repository():
    statement = (select(lds.Event, lds.EventDef)
                 .join(lds.EventDef)
                 .filter(lds.EventDef.Enabled)
                 .filter(lds.EventDef.Visible))
    with Session(engine) as session:
        results = session.execute(statement).all()
        return results


def get_event_by_id_repository(event_id: int):
    statement = (select(lds.Event, lds.EventDef)
                 .join(lds.EventDef)
                 .where(lds.Event.ID == event_id)) # noqa
    with Session(engine) as session:
        results = session.execute(statement).all()
        return results


def set_event_ack_date_repository(event_id: int):
    with Session(engine) as session:
        event = session.get(lds.Event, event_id)
        if not event:
            raise NoResultFound()
        event.AckDate = datetime.now()
        session.add(event)
        session.commit()
