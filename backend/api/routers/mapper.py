from .utils import to_dict, strip_strings_in_dict
from ..schemas import EventOut, TrendDef, TrendParam, TrendDataMultiple, TrendValue, TrendDataSingle, Trend, Node, \
    NodeOut, EditorNodeBase
from database import lds, editor


def map_lds_event_and_lds_event_def_to_event_out(lds_event: lds.Event, lds_event_def: lds.EventDef) -> EventOut:
    lds_event_dict = to_dict(lds_event)
    lds_event_def_dict = to_dict(lds_event_def)
    lds_event_def_dict.pop('ID')
    lds_event_dict.update(lds_event_def_dict)
    lds_event_dict = strip_strings_in_dict(lds_event_dict)
    return EventOut(**lds_event_dict)


def map_lds_trend_to_trend(lds_trend: lds.Trend) -> Trend:
    return Trend(**strip_strings_in_dict(to_dict(lds_trend)))


def map_trend_to_lds_trend(trend: Trend) -> lds.Trend:
    return lds.Trend(**trend.model_dump(by_alias=True))


def map_lds_trend_def_to_trend_def(lds_trend_def: lds.TrendDef) -> TrendDef:
    return TrendDef(**strip_strings_in_dict(to_dict(lds_trend_def)))


def map_trend_def_to_lds_trend_def(trend_def: TrendDef) -> lds.TrendDef:
    return lds.TrendDef(**trend_def.model_dump(by_alias=True))


def map_lds_trend_param_and_lds_trend_param_def_to_trend_param(lds_trend_param: lds.TrendParam, lds_trend_param_def: lds.TrendParamDef) -> TrendParam: # noqa
    lds_trend_param_dict = to_dict(lds_trend_param)
    lds_trend_param_def_dict = to_dict(lds_trend_param_def)
    lds_trend_param_def_dict.pop('TrendDefID')
    lds_trend_param_def_dict.pop('ID')
    lds_trend_param_dict.update(lds_trend_param_def_dict)
    return TrendParam(**strip_strings_in_dict(lds_trend_param_dict))


def map_dicts_to_trend_data_multiple(timestamps: zip, trend_values_dict: dict) -> list[TrendDataMultiple]:
    trend_datas = []
    for counter, timestamp in enumerate(timestamps):
        trend_values = [
            TrendValue(ID=trend_id, Value=trend_values_dict[trend_id][counter][0])
            for trend_id in trend_values_dict
        ]
        trend_data = TrendDataMultiple(
            Timestamp=timestamp[0],
            TimestampMs=timestamp[1],
            Data=trend_values
        )
        trend_datas.append(trend_data)

    return trend_datas


def map_tuple_to_trend_data_single(values: tuple) -> TrendDataSingle:
    return TrendDataSingle(
        Timestamp=values[1],
        TimestampMs=values[2],
        Value=values[0]
    )


def map_node_to_lds_node(node: Node) -> lds.Node:
    return lds.Node(**node.model_dump(exclude={'TrendID', 'EditorParams'}))


def map_node_to_editor_node(node_id: int, node: Node) -> editor.Node | None:
    if node.EditorParams:
        editor_node_dict = {'ID': node_id,
                            'PosX': node.EditorParams.PosX,
                            'PosY': node.EditorParams.PosY}
        return editor.Node(**editor_node_dict)
    return None


def map_lds_node_and_editor_node_to_node_out(lds_node: lds.Node, editor_node: editor.Node) -> NodeOut:
    node_out_dict = to_dict(lds_node)
    editor_params = None
    if editor_node:
        editor_node_dict = to_dict(editor_node)
        editor_node_dict.pop('ID')
        editor_params = EditorNodeBase(**editor_node_dict)
    node_out_dict.update({'EditorParams': editor_params})
    return NodeOut(**strip_strings_in_dict(node_out_dict))
