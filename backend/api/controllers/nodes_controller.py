from ast import stmt
import connexion
import six

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.node import Node  # noqa: E501
from api.models.editor_node import EditorNode  # noqa: E501
from api import util

from sqlalchemy import alias, select, delete
from ..db import session
from database.models import editor, lds


def create_node(node=None):  # noqa: E501
    """Create nodes

    Create a nodes # noqa: E501

    :param node: 
    :type node: dict | bytes

    :rtype: Information
    """

    try:
        if connexion.request.is_json:
            node = Node.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_node = lds.Node()
        db_node.Type = node.type
        db_node.TrendID = node.trend_id
        db_node.Name = node.name
        session.add(db_node)
        session.flush()

        if node.editor_params:
            db_editor_node = editor.Node()
            db_editor_node.ID = db_node.ID
            db_editor_node.PosX = node.editor_params.pos_x
            db_editor_node.PosY = node.editor_params.pos_y
            session.add(db_editor_node)
        
        session.commit()

        return get_node_by_id(db_node.ID)

    except Exception as e:
        error: Error = Error(message=str(e), code=500)
        return error, 500        

def update_node(node_id, node=None):  # noqa: E501
    """Create nodes

    Create a nodes # noqa: E501

    :param node: 
    :type node: dict | bytes

    :rtype: Information
    """

    try:
        if connexion.request.is_json:
            api_node = Node.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_node = session.get(lds.Node, node_id)
        if db_node is None:
            return Error(message="Not Found", code=404), 404

        db_node.Type = api_node.type
        db_node.TrendID = api_node.trend_id
        db_node.Name = api_node.name
        session.add(db_node)
        session.flush()

        db_editor_node = session.get(editor.Node, node_id)
        if db_editor_node is None:
            db_editor_node = editor.Node()
            db_editor_node.ID = node_id

        db_editor_node.PosX = api_node.editor_params.pos_x
        db_editor_node.PosY = api_node.editor_params.pos_y
        session.add(db_editor_node)

        session.commit()

        return get_node_by_id(db_node.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  

def delete_node_by_id(node_id):  # noqa: E501
    """Detail node

    Delete specific node # noqa: E501

    :param node_id: The id of the node to retrieve
    :type node_id: int

    :rtype: Information
    """
    try:        
        db_node = session.get(lds.Node, node_id)
        if db_node is None:
            return Error(message="Not Found", code=404), 404
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
        node = session.get(lds.Node, node_id)
        if node is None:
            return Error(message="Not Found", code=404), 404
        api_node = Node()
        api_node.id = node.ID
        api_node.type = node.Type
        api_node.trend_id = node.TrendID
        api_node.name = node.Name

        editor_node = session.get(editor.Node, node_id)
        if editor_node is not None:
            api_node.editor_params = EditorNode()
            api_node.editor_params.pos_x = editor_node.PosX
            api_node.editor_params.pos_y = editor_node.PosY

        return api_node, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_nodes():  # noqa: E501
    """List nodes

    List all nodes # noqa: E501


    :rtype: List[Node]
    """
    try:
        ln = alias(lds.Node, "ln")
        en = alias(editor.Node, "en")
        nodes = session.execute(
            select([ln, en]).outerjoin(en, en.c.ID == ln.c.ID )
        ).fetchall()

        print(nodes)

        if nodes is None:
            return Error(message="Not Found", code=500), 404

        api_nodes = []
        for node in nodes:
            api_node = Node()
            api_node.id = node.ID
            api_node.type = node.Type
            api_node.trend_id = node.TrendID
            api_node.name = node.Name
            if node.ID_1 is not None:
                api_node.editor_params = EditorNode()
                api_node.editor_params.pos_x = node.PosX
                api_node.editor_params.pos_y = node.PosY
            api_nodes.append(api_node)        


        return api_nodes, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500
