from ast import stmt
from operator import or_
import connexion
import six

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.node import Node  # noqa: E501
from api.models.editor_node import EditorNode  # noqa: E501
from api import util

from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, delete, or_
from sqlalchemy.orm import aliased
from ..db import session
from database.models import editor, lds
from .security_controller import check_permissions


def create_node(node=None, token_info={}):  # noqa: E501
    """Create nodes

    Create a nodes # noqa: E501

    :param node: 
    :type node: dict | bytes

    :rtype: Information
    """

    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            node = Node.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_node = editor.Node()
        db_node.Type = node.type
        db_node.Name = node.name                
        if node.editor_params:
            db_node.Node = editor.Node_()
            db_node.Node.PosX = node.editor_params.pos_x
            db_node.Node.PosY = node.editor_params.pos_y
        session.add(db_node)

        session.commit()

        return get_node_by_id(db_node.ID)

    except Exception as e:
        error: Error = Error(message=str(e), code=500)
        return error, 500        

def update_node(node_id, node=None, token_info={}):  # noqa: E501
    """Create nodes

    Create a nodes # noqa: E501

    :param node: 
    :type node: dict | bytes

    :rtype: Information
    """

    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_node = Node.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_node = session.get(editor.Node, node_id)
        if db_node is None:
            return Error(message="Not Found", code=404), 404
        db_node.Type = api_node.type
        db_node.Name = api_node.name  
        if api_node.editor_params is not None:
            if db_node.Node is None:
                db_node.Node = editor.Node_
            db_node.Node.PosX = api_node.editor_params.pos_x
            db_node.Node.PosY = api_node.editor_params.pos_y
        session.add(db_node)
        session.commit()

        return get_node_by_id(db_node.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  

def delete_node_by_id(node_id, token_info={}):  # noqa: E501
    """Detail node

    Delete specific node # noqa: E501

    :param node_id: The id of the node to retrieve
    :type node_id: int

    :rtype: Information
    """
    try:        
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403        

        db_node = session.get(editor.Node, node_id)
        if db_node is None:
            return Error(message="Not Found", code=404), 404

        stmt = delete(lds.Link).where(lds.Link.BeginNodeID == node_id or lds.Link.EndNodeID == node_id)
        session.execute(stmt)
        session.flush()

        if db_node.Node is not None:
            session.delete(db_node.Node)
        session.delete(db_node)
        session.commit()

        return Information(message="Success", status=200), 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_node_by_id(node_id):  # noqa: E501
    """Detail node

    Info for specific node # noqa: E501

    :param node_id: The id of the node to retrieve
    :type node_id: int

    :rtype: Node
    """
    try:
        db_node = session.get(editor.Node, node_id)
        if db_node is None:
            return Error(message="Not Found", code=404), 404
        api_node = Node()
        api_node.id = db_node.ID
        api_node.type = db_node.Type.strip()
        api_node.name = db_node.Name

        if db_node.Node is not None:
            api_node.editor_params = EditorNode()
            api_node.editor_params.pos_x = db_node.Node.PosX
            api_node.editor_params.pos_y = db_node.Node.PosY

        return api_node, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_nodes(filter_=None, filter=None):  # noqa: E501
    """List nodes

    List all nodes # noqa: E501


    :rtype: List[Node]
    """
    try:
        stmt = select(editor.Node)
        if filter_ is not None:
            stmt = apply_odata_query(stmt, filter_)        
        nodes = session.execute(stmt)

        api_nodes = []
        for bd_node, in nodes:
            api_node = Node()
            api_node.id = bd_node.ID
            api_node.type = bd_node.Type.strip()
            api_node.name = bd_node.Name
            if bd_node.Node is not None:
                api_node.editor_params = EditorNode()
                api_node.editor_params.pos_x = bd_node.Node.PosX
                api_node.editor_params.pos_y = bd_node.Node.PosY
            api_nodes.append(api_node)           


        return api_nodes, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500
