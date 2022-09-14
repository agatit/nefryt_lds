import connexion
import six

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.pipeline import Pipeline  # noqa: E501
from api.models.pipeline_param import PipelineParam  # noqa: E501
from api.models.pipeline_param_def import PipelineParamDef  # noqa: E501
from api.models.editor_pipeline import EditorPipeline  # noqa: E501
from api import util

from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import aliased
from ..db import session
from database.models import editor, lds
from .security_controller import check_permissions


def create_pipeline(pipeline=None, token_info={}):  # noqa: E501
    """Create pipelines

    Create a pipelines # noqa: E501

    :param pipeline: 
    :type pipeline: dict | bytes

    :rtype: Information
    """

    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_pipeline: Pipeline = Pipeline.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_pipeline: lds.Pipeline = lds.Pipeline()       
        db_pipeline.Name = api_pipeline.name
        db_pipeline.BeginPos = api_pipeline.begin_pos
        session.add(db_pipeline)
        session.flush()

        if api_pipeline.editor_params is not None:
            db_editor_pipeline: editor.Pipeline = editor.Pipeline()
            db_editor_pipeline.ID = api_pipeline.id
            db_editor_pipeline.AreaHeight = api_pipeline.editor_params.area_height
            db_editor_pipeline.AreaWidth = api_pipeline.editor_params.area_width
            db_editor_pipeline.AreaHeightDivision = api_pipeline.editor_params.area_height_division
            db_editor_pipeline.AreaWidthDivision = api_pipeline.editor_params.area_width_division
            session.add(db_editor_pipeline)
        
        session.commit()

        return get_pipeline_by_id(db_pipeline.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500        

def update_pipeline(pipeline_id, pipeline=None, token_info={}):  # noqa: E501
    """Create pipelines

    Create a pipelines # noqa: E501

    :param pipeline: 
    :type pipeline: dict | bytes

    :rtype: Information
    """

    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_pipeline = Pipeline.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_pipeline = session.get(lds.Pipeline, pipeline_id)
        if db_pipeline is None:
            return Error(message="Not Found", code=404), 404       
        db_pipeline.Name = api_pipeline.name
        db_pipeline.BeginPos = api_pipeline.begin_pos
        session.add(db_pipeline)
        session.flush()

        db_editor_pipeline = session.get(editor.Pipeline, pipeline_id)
        if db_editor_pipeline is None:
            db_editor_pipeline = editor.Pipeline()
            db_editor_pipeline.ID = pipeline_id

        db_editor_pipeline.AreaHeight = api_pipeline.editor_params.area_height
        db_editor_pipeline.AreaWidth = api_pipeline.editor_params.area_width
        db_editor_pipeline.AreaHeightDivision = api_pipeline.editor_params.area_height_division
        db_editor_pipeline.AreaWidthDivision = api_pipeline.editor_params.area_width_division
        session.add(db_editor_pipeline)

        session.commit()

        return get_pipeline_by_id(db_pipeline.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  

def delete_pipeline_by_id(pipeline_id, token_info={}):  # noqa: E501
    """Detail pipeline

    Delete specific pipeline # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int

    :rtype: Information
    """
    try:        
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        db_pipeline = session.get(lds.Pipeline, pipeline_id)
        if db_pipeline is None:
            return Error(message="Not Found", code=404), 404
        session.delete(db_pipeline)
        session.commit()

        return Information(message="Success", status=200), 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_pipeline_by_id(pipeline_id):  # noqa: E501
    """Detail pipeline

    Info for specific pipeline # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int

    :rtype: pipeline
    """
    try:
        db_pipeline = session.get(lds.Pipeline, pipeline_id)
        if db_pipeline is None:
            return Error(message="Not Found", code=404), 404
        api_pipeline = Pipeline()
        api_pipeline.id = db_pipeline.ID
        api_pipeline.name = db_pipeline.Name
        api_pipeline.begin_pos = db_pipeline.BeginPos

        db_editor_pipeline = session.get(editor.Pipeline, pipeline_id)
        if db_editor_pipeline is not None:
            api_pipeline.editor_params = EditorPipeline()
            api_pipeline.editor_params.area_height = db_editor_pipeline.AreaHeight
            api_pipeline.editor_params.area_width = db_editor_pipeline.AreaWidth
            api_pipeline.editor_params.area_height_division = db_editor_pipeline.AreaHeightDivision
            api_pipeline.editor_params.area_width_division = db_editor_pipeline.AreaWidthDivision

        return api_pipeline, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_pipelines(filter_=None, filter=None):  # noqa: E501
    """List pipelines

    List all pipelines # noqa: E501


    :rtype: List[pipeline]
    """
    try:
        ln = aliased(lds.Pipeline)
        en = aliased(editor.Pipeline)
        stmt = select(ln, en).select_from(ln).outerjoin(en, en.ID == ln.ID)
        if filter_ is not None:
            stmt = apply_odata_query(stmt, filter_)        
        db_pipelines = session.execute(stmt)        

        api_pipelines = []
        for lds_pipeline, editor_pipeline in db_pipelines:
            api_pipeline = Pipeline()
            api_pipeline.id = lds_pipeline.ID
            api_pipeline.name = lds_pipeline.Name
            api_pipeline.begin_pos = lds_pipeline.BeginPos
            if editor_pipeline is not None:
                api_pipeline.editor_params = EditorPipeline()
                api_pipeline.editor_params.area_height = editor_pipeline.AreaHeight
                api_pipeline.editor_params.area_width = editor_pipeline.AreaWidth
                api_pipeline.editor_params.area_height_division = editor_pipeline.AreaHeightDivision
                api_pipeline.editor_params.area_width_division = editor_pipeline.AreaWidthDivision
            api_pipelines.append(api_pipeline)        

        return api_pipelines, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_pipeline_param_by_id(pipeline_id, pipeline_param_def_id):  # noqa: E501
    """Gets pipeline param detail

    Info for specific pipeline param # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int
    :param param_id: The id of the param to retrieve
    :type param_id: int

    :rtype: PipelineParam
    """
    try:
        db_pipeline_param = session.get(lds.PipelineParam, (pipeline_param_def_id, pipeline_id))
        if db_pipeline_param is None:
            return Error(message="Not Found", code=404), 404

        api_pipeline_param = PipelineParam()
        api_pipeline_param.pipeline_id = db_pipeline_param.PipelineID
        api_pipeline_param.pipeline_param_def_id = db_pipeline_param.PipelineParamDefID.strip()
        api_pipeline_param.value = db_pipeline_param.Value

        return api_pipeline_param, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_pipeline_params(pipeline_id, filter_=None, filter=None):  # noqa: E501
    """List pipeline params

    List all pipeline params # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int

    :rtype: List[PipelineParam]
    """

    try:

        stmt = select([lds.PipelineParam, lds.PipelineParamDef]) \
            .select_from(lds.PipelineParamDef) \
            .outerjoin(lds.PipelineParam, \
                    and_(lds.PipelineParamDef.ID == lds.PipelineParam.PipelineParamDefID, lds.PipelineParam.PipelineID == pipeline_id) \
                )  
        if filter_ is not None:
            stmt = apply_odata_query(stmt, filter_)                

        db_pipeline_params = session.execute(stmt)

        api_pipeline_params = []
        for db_pipeline_param, db_pipeline_param_def in db_pipeline_params:
            api_pipeline_param = PipelineParam()
            api_pipeline_param.pipeline_id = pipeline_id
            api_pipeline_param.pipeline_param_def_id = db_pipeline_param_def.ID.strip()            
            api_pipeline_param.name = db_pipeline_param_def.Name
            api_pipeline_param.data_type = db_pipeline_param_def.DataType.strip()
            if db_pipeline_param is not None:
                api_pipeline_param.value = db_pipeline_param.Value
            api_pipeline_params.append(api_pipeline_param)

        return api_pipeline_params, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def update_pipeline_param(pipeline_id, pipeline_param_def_id, pipeline_param=None, token_info={}):  # noqa: E501
    """Update pipeline params

    Updates pipeline param # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int
    :param pipeline_param: 
    :type pipeline_param: dict | bytes

    :rtype: Information
    """
    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403
            
        if connexion.request.is_json:
            api_pipeline_param = PipelineParam.from_dict(connexion.request.get_json())  # noqa: E501

        db_pipeline_param = session.get(lds.PipelineParam, (pipeline_param_def_id, pipeline_id))
        if db_pipeline_param is None:
            return Error(message="Not Found", code=404), 404

        
        db_pipeline_param.Value = api_pipeline_param.value
        session.add(db_pipeline_param)

        session.commit()

        return get_pipeline_param_by_id(db_pipeline_param.PipelineID, db_pipeline_param.PipelineParamDefID)

    except Exception as e:
        return Error(message=str(e), code=500), 500          
