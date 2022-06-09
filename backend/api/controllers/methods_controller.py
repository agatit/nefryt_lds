import connexion
import six

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.inline_response200 import InlineResponse200  # noqa: E501
from api.models.method import Method  # noqa: E501
from api.models.method_param import MethodParam  # noqa: E501
from api import util


def create_method(pipeline_id, method=None):  # noqa: E501
    """Creates method

    Creates a  method # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int
    :param method: 
    :type method: dict | bytes

    :rtype: Method
    """
    if connexion.request.is_json:
        method = Method.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def delete_method_by_id(pipeline_id, method_id):  # noqa: E501
    """Deletes  method

    Deletes specific  method # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int
    :param method_id: The id of the pipeline method to retrieve
    :type method_id: int

    :rtype: Information
    """
    return 'do some magic!'


def get_method_by_id(pipeline_id, method_id):  # noqa: E501
    """Gets  method details

    Info for specific  method # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int
    :param method_id: The id of the pipeline method to retrieve
    :type method_id: int

    :rtype: InlineResponse200
    """
    return 'do some magic!'


def list_method_params(pipeline_id, method_id):  # noqa: E501
    """List pipelnie method params

    List all  method params # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int
    :param method_id: The id of the pipeline method to retrieve
    :type method_id: int

    :rtype: List[MethodParam]
    """
    return 'do some magic!'


def list_methods(pipeline_id):  # noqa: E501
    """List pipelnie methods

    List all methods # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int

    :rtype: List[Method]
    """
    return 'do some magic!'


def update_method(pipeline_id, method_id, method=None):  # noqa: E501
    """Updates method

    Updates  method # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int
    :param method_id: The id of the pipeline method to retrieve
    :type method_id: int
    :param method: 
    :type method: dict | bytes

    :rtype: Method
    """
    if connexion.request.is_json:
        method = Method.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_method_params(pipeline_id, method_id, method_param_def_id, method_param=None):  # noqa: E501
    """Put pipelnie method params

    Put  method params # noqa: E501

    :param pipeline_id: The id of the pipeline to retrieve
    :type pipeline_id: int
    :param method_id: The id of the pipeline method to retrieve
    :type method_id: int
    :param method_param_def_id: The id of the param to retrieve
    :type method_param_def_id: str
    :param method_param: 
    :type method_param: list | bytes

    :rtype: Information
    """
    if connexion.request.is_json:
        method_param = [MethodParam.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'
