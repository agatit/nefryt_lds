from api.routers.utils import to_dict, strip_strings_in_dict
from ...schemas import api, base
from database import lds, editor


def map_lds_event_and_lds_event_def_to_api_event(lds_event: lds.Event, lds_event_def: lds.EventDef) -> api.Event:
    lds_event_dict = to_dict(lds_event)
    lds_event_def_dict = to_dict(lds_event_def)
    lds_event_def_dict.pop('ID')
    lds_event_dict.update(lds_event_def_dict)
    lds_event_dict = strip_strings_in_dict(lds_event_dict)
    return api.Event(**lds_event_dict)


def map_lds_trend_param_and_lds_trend_param_def_to_api_trend_param(lds_trend_param: lds.TrendParam | None, lds_trend_param_def: lds.TrendParamDef, trend_id: int) -> api.TrendParam:
    if lds_trend_param is None:
        lds_trend_param_dict = {
            'TrendID': trend_id,
            'TrendParamDefID': lds_trend_param_def.ID,
            'Value': None
        }
    else:
        lds_trend_param_dict = to_dict(lds_trend_param)
    lds_trend_param_def_dict = to_dict(lds_trend_param_def)
    lds_trend_param_def_dict.pop('TrendDefID')
    lds_trend_param_def_dict.pop('ID')
    lds_trend_param_dict.update(lds_trend_param_def_dict)
    return api.TrendParam(**strip_strings_in_dict(lds_trend_param_dict))


def map_dicts_to_trend_data_multiple(timestamps: zip, trend_values_dict: dict) -> list[api.TrendDataMultiple]:
    trend_data_list = []
    for counter, timestamp in enumerate(timestamps):
        trend_values = [
            api.TrendValue(ID=trend_id, Value=trend_values_dict[trend_id][counter][0])
            for trend_id in trend_values_dict
        ]
        trend_data = api.TrendDataMultiple(
            Timestamp=timestamp[0],
            TimestampMs=timestamp[1],
            Data=trend_values
        )
        trend_data_list.append(trend_data)

    return trend_data_list


def map_tuple_to_trend_data_single(values: tuple) -> api.TrendDataSingle:
    return api.TrendDataSingle(
        Timestamp=values[1],
        TimestampMs=values[2],
        Value=values[0]
    )


def map_node_to_lds_node(node: api.NodeCreate) -> lds.Node:
    return lds.Node(**node.model_dump(exclude={'TrendID', 'EditorParams'}))


def map_node_to_editor_node(node_id: int, node: api.NodeCreate) -> editor.Node | None:
    if node.EditorParams:
        editor_node_dict = {'ID': node_id,
                            'PosX': node.EditorParams.PosX,
                            'PosY': node.EditorParams.PosY}
        return editor.Node(**editor_node_dict)
    return None


def map_lds_node_and_editor_node_to_api_node(lds_node: lds.Node, editor_node: editor.Node) -> api.Node:
    api_node_dict = to_dict(lds_node)
    editor_params = None
    if editor_node:
        editor_node_dict = to_dict(editor_node)
        editor_node_dict.pop('ID')
        editor_params = base.EditorNode(**editor_node_dict)
    api_node_dict.update({'EditorParams': editor_params})
    return api.Node(**strip_strings_in_dict(api_node_dict))


def map_lds_simulation_param_and_lds_simulation_param_def_to_api_simulation_param\
                (lds_simulation_param: lds.SimulationParam | None, lds_simulation_param_def: lds.SimulationParamDef, simulation_id: int) -> api.SimulationParam:
    if lds_simulation_param is None:
        lds_simulation_param_dict = {
            'SimulationID': simulation_id,
            'SimulationParamDefID': lds_simulation_param_def.ID,
            'Value': None
        }
    else:
        lds_simulation_param_dict = to_dict(lds_simulation_param)
        lds_simulation_param_dict.pop('SimulationDefID')
    lds_simulation_param_def_dict = to_dict(lds_simulation_param_def)
    lds_simulation_param_def_dict.pop('SimulationDefID')
    lds_simulation_param_def_dict.pop('ID')
    api_simulation_param_dict = lds_simulation_param_dict | lds_simulation_param_def_dict
    return api.SimulationParam(**strip_strings_in_dict(api_simulation_param_dict))


def map_simulation_param_base_to_lds_simulation_param(simulation_param: api.SimulationParamCreate, lds_simulation: lds.Simulation) -> lds.SimulationParam:
    return lds.SimulationParam(**simulation_param.model_dump()
                                     | {'SimulationDefID': lds_simulation.SimulationDefID, 'SimulationID': lds_simulation.ID})


def map_lds_simulation_data_to_api_simulation_data(simulation_data_list: list[lds.SimulationData], distances: list[int]) -> api.SimulationData:
    iter_lds_simulation_data = iter(simulation_data_list)
    lds_simulation_data = next(iter_lds_simulation_data, None)
    api_simulation_data_dict = {
        'SimulationID': lds_simulation_data.SimulationID,
        'Time': lds_simulation_data.Time,
        'Data': []
    }
    for distance in distances:
        if not lds_simulation_data:
            api_simulation_data_dict['Data'].append(
                base.SimulationData(Distance=distance, Data=None)
            )
        elif lds_simulation_data.Distance == distance:
            api_simulation_data_dict['Data'].append(
                base.SimulationData(Distance=distance, Data=lds_simulation_data.Data)
            )
            lds_simulation_data = next(iter_lds_simulation_data, None)
        else:
            api_simulation_data_dict['Data'].append(
                base.SimulationData(Distance=distance, Data=None)
            )

    return api.SimulationData(**api_simulation_data_dict)

def map_lds_pipeline_param_and_lds_pipeline_param_def_to_api_pipeline_param\
                (lds_pipeline_param: lds.PipelineParam | None, lds_pipeline_param_def: lds.PipelineParamDef, pipeline_id: int) -> api.PipelineParam:
    if lds_pipeline_param is None:
        lds_pipeline_param_dict = {
            'PipelineID': pipeline_id,
            'PipelineParamDefID': lds_pipeline_param_def.ID,
            'Value': None
        }
    else:
        lds_pipeline_param_dict = to_dict(lds_pipeline_param)
    lds_pipeline_param_def_dict = to_dict(lds_pipeline_param_def)
    lds_pipeline_param_def_dict.pop('ID')
    api_pipeline_param_dict = lds_pipeline_param_dict | lds_pipeline_param_def_dict
    return api.PipelineParam(**strip_strings_in_dict(api_pipeline_param_dict))


def map_pipeline_param_base_to_lds_pipeline_param(pipeline_param: api.PipelineParamCreate, lds_pipeline: lds.Pipeline) -> lds.PipelineParam:
    return lds.PipelineParam(**pipeline_param.model_dump() | {'PipelineID': lds_pipeline.ID})


def map_lds_method_param_and_lds_method_param_def_to_api_method_param\
                (lds_method_param: lds.MethodParam | None, lds_method_param_def: lds.MethodParamDef, method_id: int) -> api.MethodParam:
    if lds_method_param is None:
        lds_method_param_dict = {
            'MethodID': method_id,
            'MethodParamDefID': lds_method_param_def.ID,
            'Value': None
        }
    else:
        lds_method_param_dict = to_dict(lds_method_param)
    lds_method_param_def_dict = to_dict(lds_method_param_def)
    lds_method_param_def_dict.pop('ID')
    api_method_param_dict = lds_method_param_dict | lds_method_param_def_dict
    return api.MethodParam(**strip_strings_in_dict(api_method_param_dict))


def map_method_param_base_to_lds_method_param(method_param: api.MethodParamCreate, lds_method: lds.Method) -> lds.MethodParam:
    return lds.MethodParam(**method_param.model_dump() | {'MethodID': lds_method.ID})
