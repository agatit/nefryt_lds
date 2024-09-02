from ..schemas import Event, EventDef, TrendDef, TrendParam
from database import lds
from ..schemas.trend import Trend

# todo: czy wszystkie mappery są potrzebne check?


def to_dict(o) -> dict:
    return {c.name: getattr(o, c.name) for c in o.__table__.columns}


def map_lds_event_and_lds_event_def_to_event(lds_event: lds.Event, lds_event_def: lds.EventDef) -> Event:
    lds_event_dict = to_dict(lds_event)
    lds_event_def_dict = to_dict(lds_event_def)
    lds_event_def_dict.pop('ID')
    lds_event_dict.update(lds_event_def_dict)
    return Event(**lds_event_dict)


def map_lds_trend_to_trend(lds_trend: lds.Trend) -> Trend:
    lds_trend_dict = to_dict(lds_trend)
    return Trend(**lds_trend_dict)


def map_trend_to_lds_trend(trend: Trend) -> lds.Trend:
    trend_dict = to_dict(trend)
    return lds.Trend(**trend_dict)


def map_event_def_to_lds_event_def(event_def: EventDef) -> lds.EventDef:
    return lds.EventDef(**event_def.model_dump(by_alias=True))


def map_lds_event_def_to_event_def(lds_event_def: lds.EventDef) -> EventDef:
    return EventDef(**to_dict(lds_event_def))


def map_lds_trend_def_to_trend_def(lds_trend_def: lds.TrendDef) -> TrendDef:
    return TrendDef(**to_dict(lds_trend_def[0]))


def map_trend_def_to_lds_trend_def(trend_def: TrendDef) -> lds.TrendDef:
    return lds.TrendDef(**trend_def.model_dump(by_alias=True))


def map_lds_trend_param_and_lds_trend_param_def_to_trend_param(lds_trend_param: lds.TrendParam, lds_trend_param_def: lds.TrendParamDef) -> TrendParam:
    lds_trend_param_dict = to_dict(lds_trend_param)
    lds_trend_param_def_dict = to_dict(lds_trend_param_def)
    lds_trend_param_def_dict.pop('TrendDefID')
    lds_trend_param_def_dict.pop('ID')
    lds_trend_param_dict.update(lds_trend_param_def_dict)
    return TrendParam(**lds_trend_param_dict)
