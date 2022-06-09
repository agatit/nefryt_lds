import connexion
import six

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.pipeline import Pipeline  # noqa: E501
from api.models.editor_pipeline import EditorPipeline  # noqa: E501
from api import util

from sqlalchemy import alias, select, delete
from database import db
from database.models import editor, lds


def create_pipeline(pipeline=None):  # noqa: E501
    """Create pipelines

    Create a pipelines # noqa: E501

    :param pipeline: 
    :type pipeline: dict | bytes

    :rtype: Information
    """

    try:
        if connexion.request.is_json:
            api_pipeline: Pipeline = Pipeline.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_pipeline: lds.Pipeline = lds.Pipeline()       
        db_pipeline.Name = api_pipeline.name
        db_pipeline.BeginPos = api_pipeline.begin_pos
        db.session.add(db_pipeline)
        db.session.flush()

        if api_pipeline.editor_params is not None:
            db_editor_pipeline: editor.Pipeline = editor.Pipeline()
            db_editor_pipeline.ID = api_pipeline.id
            db_editor_pipeline.AreaHeight = api_pipeline.editor_params.area_height
            db_editor_pipeline.AreaWidth = api_pipeline.editor_params.area_width
            db_editor_pipeline.AreaHeightDivision = api_pipeline.editor_params.area_height_division
            db_editor_pipeline.AreaWidthDivision = api_pipeline.editor_params.area_width_division
            db.session.add(db_editor_pipeline)
        
        db.session.commit()

        return get_pipeline_by_id(db_pipeline.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500        

def update_pipeline(pipeline_id, pipeline=None):  # noqa: E501
    """Create pipelines

    Create a pipelines # noqa: E501

    :param pipeline: 
    :type pipeline: dict | bytes

    :rtype: Information
    """

    try:
        if connexion.request.is_json:
            api_pipeline = Pipeline.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_pipeline = db.session.get(lds.Pipeline, pipeline_id)
        if db_pipeline is None:
            return Error(message="Not Found", code=404), 404       
        db_pipeline.Name = api_pipeline.name
        db_pipeline.BeginPos = api_pipeline.begin_pos
        db.session.add(db_pipeline)
        db.session.flush()

        db_editor_pipeline = db.session.get(editor.Pipeline, pipeline_id)
        if db_editor_pipeline is None:
            db_editor_pipeline = editor.Pipeline()
            db_editor_pipeline.ID = pipeline_id

        db_editor_pipeline.AreaHeight = api_pipeline.editor_params.area_height
        db_editor_pipeline.AreaWidth = api_pipeline.editor_params.area_width
        db_editor_pipeline.AreaHeightDivision = api_pipeline.editor_params.area_height_division
        db_editor_pipeline.AreaWidthDivision = api_pipeline.editor_params.area_width_division
        db.session.add(db_editor_pipeline)

        db.session.commit()

        return get_pipeline_by_id(db_pipeline.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  

def delete_pipeline_by_id(pipeline_id):  # noqa: E501
    """Detail pipeline

    Delete specific pipeline # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int

    :rtype: Information
    """
    try:        
        db_pipeline = db.session.get(lds.Pipeline, pipeline_id)
        if db_pipeline is None:
            return Error(message="Not Found", code=404), 404
        db.session.delete(db_pipeline)
        db.session.commit()

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
        db_pipeline = db.session.get(lds.Pipeline, pipeline_id)
        if db_pipeline is None:
            return Error(message="Not Found", code=404), 404
        api_pipeline = Pipeline()
        api_pipeline.id = db_pipeline.ID
        api_pipeline.name = db_pipeline.Name
        api_pipeline.begin_pos = db_pipeline.BeginPos

        db_editor_pipeline = db.session.get(editor.Pipeline, pipeline_id)
        if db_editor_pipeline is not None:
            api_pipeline.editor_params = EditorPipeline()
            api_pipeline.editor_params.area_height = db_editor_pipeline.AreaHeight
            api_pipeline.editor_params.area_width = db_editor_pipeline.AreaWidth
            api_pipeline.editor_params.area_height_division = db_editor_pipeline.AreaHeightDivision
            api_pipeline.editor_params.area_width_division = db_editor_pipeline.AreaWidthDivision

        return api_pipeline, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_pipelines():  # noqa: E501
    """List pipelines

    List all pipelines # noqa: E501


    :rtype: List[pipeline]
    """
    try:
        ln = alias(lds.Pipeline, "ln")
        en = alias(editor.Pipeline, "en")  
        db_pipelines = db.session.execute(
            select(ln, en).select_from(ln).outerjoin(en, en.c.ID == ln.c.ID )
        ).fetchall()        

        if db_pipelines is None:
            return Error(message="Not Found", code=500), 404

        api_pipelines = []
        for db_pipeline in db_pipelines:
            api_pipeline = Pipeline()
            api_pipeline.id = db_pipeline.ID
            api_pipeline.name = db_pipeline.Name
            api_pipeline.begin_pos = db_pipeline.BeginPos
            if db_pipeline.ID_1 is not None:
                api_pipeline.editor_params = EditorPipeline()
                api_pipeline.editor_params.area_height = db_pipeline.AreaHeight
                api_pipeline.editor_params.area_width = db_pipeline.AreaWidth
                api_pipeline.editor_params.area_height_division = db_pipeline.AreaHeightDivision
                api_pipeline.editor_params.area_width_division = db_pipeline.AreaWidthDivision
            api_pipelines.append(api_pipeline)        

        return api_pipelines, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500
