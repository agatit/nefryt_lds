from ..schemas import Event, EventDef, TrendDef, TrendParam, TrendData, TrendValue, Link
from database import lds
from ..schemas.trend import Trend


def to_dict(o) -> dict:
    return {c.name: getattr(o, c.name) for c in o.__table__.columns}


def strip_strings_in_dict(d: dict) -> dict:
    return {k: v.strip() if isinstance(v, str) else v for k, v in d.items()}


def map_lds_event_and_lds_event_def_to_event(lds_event: lds.Event, lds_event_def: lds.EventDef) -> Event:
    lds_event_dict = to_dict(lds_event)
    lds_event_def_dict = to_dict(lds_event_def)
    lds_event_def_dict.pop('ID')
    lds_event_dict.update(lds_event_def_dict)
    lds_event_dict = strip_strings_in_dict(lds_event_dict)
    return Event(**lds_event_dict)


def map_lds_trend_to_trend(lds_trend: lds.Trend) -> Trend:
    return Trend(**strip_strings_in_dict(to_dict(lds_trend)))


def map_trend_to_lds_trend(trend: Trend) -> lds.Trend:
    return lds.Trend(**trend.model_dump(by_alias=True))


def map_event_def_to_lds_event_def(event_def: EventDef) -> lds.EventDef:
    return lds.EventDef(**event_def.model_dump(by_alias=True))


def map_lds_event_def_to_event_def(lds_event_def: lds.EventDef) -> EventDef:
    return EventDef(**strip_strings_in_dict(to_dict(lds_event_def)))


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
    return TrendParam(**strip_strings_in_dict(lds_trend_param_dict))


def map_dicts_to_trend_data(timestamps: list[dict], trend_values_dict: dict) -> list[TrendData]:
    trend_datas = []
    for counter, timestamp in enumerate(timestamps):
        trend_values = [
            TrendValue(ID=trend_id, Value=trend_values_dict[trend_id][counter][0])
            for trend_id in trend_values_dict
        ]
        trend_data = TrendData(
            Timestamp=timestamp['Timestamp'],
            TimestampMs=timestamp['TimestampMs'],
            Data=trend_values
        )
        trend_datas.append(trend_data)

    return trend_datas


def map_lds_link_to_link(lds_link: lds.Link) -> Link:
    return Link(**to_dict(lds_link))


def map_link_to_lds_link(link: Link) -> lds.Link:
    return lds.Link(**link.model_dump(by_alias=True))
