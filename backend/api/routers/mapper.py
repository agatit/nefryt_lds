from ..schemas import Event
from database import lds


def to_dict(o) -> dict:
    return {c.name: getattr(o, c.name) for c in o.__table__.columns}


def map_lds_event_and_lds_event_def_to_event(lds_event: lds.Event, lds_event_def: lds.EventDef) -> Event:
    lds_event_dict = to_dict(lds_event)
    lds_event_def_dict = to_dict(lds_event_def)
    lds_event_def_dict.pop('ID')
    lds_event_dict.update(lds_event_def_dict)
    return Event(**lds_event_dict)


# def map_lds_trend_to_trend(lds_trend: lds.Trend) -> Trend:
#     lds_trend_dict = to_dict(lds_trend)
#     print(lds_trend_dict)
#     return Trend(**lds_trend_dict)
#
#
# def map_trend_to_lds_trend(trend: Trend) -> lds.Trend:
#     trend_dict = to_dict(trend)
#     print(trend_dict)
#     return lds.Trend(**trend_dict)
