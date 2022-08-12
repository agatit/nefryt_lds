import connexion

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.method import Method  # noqa: E501
from api.models.method_param import MethodParam  # noqa: E501
from api.models.method_def import MethodDef  # noqa: E501
from api import util

from sqlalchemy import alias, select, and_
from ..db import session
from database.models import lds
from .security_controller import check_permissions


def create_method(method=None, token_info={}):  # noqa: E501
    """Create method

    Create a method # noqa: E501

    :param method: 
    :type method: dict | bytes

    :rtype: Information
    """

    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_method = Method.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_method = lds.Method()

        db_method.Name = api_method.name
        db_method.MethodDefID = api_method.method_def_id  
        session.add(db_method)
        
        session.commit()

        return get_method_by_id(db_method.ID)

    except Exception as e:
        error: Error = Error(message=str(e), code=500)
        return error, 500   


def delete_method_by_id(pipeline_id, method_id, token_info={}):  # noqa: E501
    """Deletes method

    Deletes specific method # noqa: E501

    :param method_id: The id of the method to retrieve
    :type method_id: int

    :rtype: Information
    """
    try:        
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        db_method = session.get(lds.Method, method_id)
        if db_method is None:
            return Error(message="Not Found", code=404), 404
        session.delete(db_method)
        session.commit()

        return Information(message="Success", status=200), 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_method_by_id(pipeline_id, method_id):  # noqa: E501
    """Detail method

    Info for specific method # noqa: E501

    :param method_id: The id of the method to retrieve
    :type method_id: int

    :rtype: Method
    """
    try:
        db_method = session.get(lds.Method, method_id)
        if db_method is None:
            return Error(message="Not Found", code=404), 404

        api_method = Method()
        api_method.id = db_method.ID
        api_method.name = db_method.Name
        api_method.method_def_id = db_method.MethodDefID.strip()
        return api_method, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def update_method(pipeline_id, method_id, method=None, token_info={}):  # noqa: E501
    """Update method

    Update a method # noqa: E501

    :param method: 
    :type method: dict | bytes

    :rtype: Information
    """
    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_method = Method.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_method = session.get(lds.Method, method_id)
        if db_method is None:
            return Error(message="Not Found", code=404), 404

        db_method.Name = api_method.name
        db_method.MethodDefID = api_method.method_def_id
        session.add(db_method)

        session.commit()

        return get_method_by_id(db_method.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  


def list_methods(pipeline_id):  # noqa: E501
    """List methods

    List all methods # noqa: E501


    :rtype: List[Method]
    """
    try:
        stmt = select(lds.Method).where(lds.Method.PipelineID == pipeline_id)
        db_methods = session.execute(stmt)

        api_methods = []
        for db_method, in db_methods:
            api_method = Method()
            api_method.id = db_method.ID
            api_method.name = db_method.Name
            api_method.method_def_id = db_method.MethodDefID.strip()
            api_methods.append(api_method)        

        return api_methods, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_method_param_by_id(pipeline_id, method_id, method_param_def_id):  # noqa: E501
    """Gets method param detail

    Info for specific method param # noqa: E501

    :param method_id: The id of the method to retrieve
    :type method_id: int
    :param param_id: The id of the param to retrieve
    :type param_id: int

    :rtype: MethodParam
    """
    try:
        db_method_param = session.get(lds.MethodParam, (method_param_def_id, method_id))
        if db_method_param is None:
            return Error(message="Not Found", code=404), 404

        api_method_param = MethodParam()
        api_method_param.method_id = db_method_param.MethodID
        api_method_param.method_param_def_id = db_method_param.MethodParamDefID.strip()
        api_method_param.value = db_method_param.Value

        return api_method_param, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_method_params(pipeline_id, method_id):  # noqa: E501
    """List method params

    List all method params # noqa: E501

    :param method_id: The id of the method to retrieve
    :type method_id: int

    :rtype: List[MethodParam]
    """

    try:
        # select t.ID, tpd.ID, tpd.Name, tp.Value, tpd.DataType
        #    from lds.Method t
        #    left join lds.MethodParamDef tpd on t.MethodDefID = tpd.MethodDefID
        #    left join lds.MethodParam tp on tpd.ID = tp.MethodParamDefID and t.ID = tp.MethodID
        # where
        #     t.ID = 101

        tp = alias(lds.MethodParam, "tp")
        t = alias(lds.Method, "t")
        tpd = alias(lds.MethodParamDef, "tpd")
        
        stmt = select(t.c.ID.label("MethodID"), tpd.c.ID.label("MethodParamDefID"), tpd.c.Name, tp.c.Value, tpd.c.DataType) \
            .select_from(t) \
            .outerjoin(tpd, t.c.MethodDefID == tpd.c.MethodDefID ) \
            .outerjoin(tp, and_(tpd.c.ID == tp.c.MethodParamDefID, t.c.ID == tp.c.MethodID)) \
            .where(t.c.ID == method_id)

        db_method_params = session.execute(stmt)

        api_method_params = []
        for db_method_param in db_method_params:
            api_method_param = MethodParam()
            api_method_param.method_id = db_method_param.MethodID
            api_method_param.method_param_def_id = db_method_param.MethodParamDefID.strip()
            api_method_param.value = db_method_param.Value
            api_method_param.name = db_method_param.Name
            api_method_param.data_type = db_method_param.DataType.strip()
            api_method_params.append(api_method_param)

        return api_method_params, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def update_method_param(pipeline_id, method_id, method_param_def_id, method_param=None, token_info={}):  # noqa: E501
    """Update method params

    Updates method param # noqa: E501

    :param method_id: The id of the method to retrieve
    :type method_id: int
    :param method_param: 
    :type method_param: dict | bytes

    :rtype: Information
    """
    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_method_param = MethodParam.from_dict(connexion.request.get_json())  # noqa: E501

        db_method_param = session.get(lds.MethodParam, (method_param_def_id, method_id))
        if db_method_param is None:
            return Error(message="Not Found", code=404), 404

        
        db_method_param.Value = api_method_param.value
        session.add(db_method_param)

        session.commit()

        return get_method_param_by_id(db_method_param.MethodID, db_method_param.MethodParamDefID)

    except Exception as e:
        return Error(message=str(e), code=500), 500          


def list_method_defs():  # noqa: E501
    """List methods

    List all methods # noqa: E501


    :rtype: List[Method]
    """
    try:
        methods = session.execute(select(lds.MethodDef))

        api_methods = []
        for method, in methods:
            api_method = MethodDef()
            api_method.id = method.ID.strip()
            api_method.name = method.Name
            api_methods.append(api_method)        

        return api_methods, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500    
