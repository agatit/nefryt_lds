from ast import stmt
import connexion
import six

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.link import Link  # noqa: E501
from api import util

from sqlalchemy import alias, select, delete
from ..db import session
from database.models import lds


def create_link(link=None):  # noqa: E501
    """Create links

    Create a links # noqa: E501

    :param link: 
    :type link: dict | bytes

    :rtype: Information
    """

    try:
        if connexion.request.is_json:
            api_link = Link.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_link = lds.Link()
        db_link.BeginNodeID = api_link.begin_node_id
        db_link.EndNodeID = api_link.end_node_id
        db_link.Length = api_link.length
        session.add(db_link)
        
        session.commit()

        return get_link_by_id(db_link.ID)

    except Exception as e:
        error: Error = Error(message=str(e), code=500)
        return error, 500        

def update_link(link_id, link=None):  # noqa: E501
    """Create links

    Create a links # noqa: E501

    :param link: 
    :type link: dict | bytes

    :rtype: Information
    """

    try:
        if connexion.request.is_json:
            api_link = Link.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_link = session.get(lds.Link, link_id)
        if db_link is None:
            return Error(message="Not Found", code=404), 404

        db_link.BeginNodeID = api_link.begin_node_id
        db_link.EndNodeID = api_link.end_node_id
        db_link.Length = api_link.length
        session.add(db_link)

        session.commit()

        return get_link_by_id(db_link.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  

def delete_link_by_id(link_id):  # noqa: E501
    """Detail link

    Delete specific link # noqa: E501

    :param link_id: The id of the link to retrieve
    :type link_id: int

    :rtype: Information
    """
    try:        
        db_link = session.get(lds.Link, link_id)
        if db_link is None:
            return Error(message="Not Found", code=404), 404
        session.delete(db_link)
        session.commit()

        return Information(message="Success", status=200), 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_link_by_id(link_id):  # noqa: E501
    """Detail link

    Info for specific link # noqa: E501

    :param link_id: The id of the link to retrieve
    :type link_id: int

    :rtype: Link
    """
    try:
        link = session.get(lds.Link, link_id)
        if link is None:
            return Error(message="Not Found", code=404), 404
        api_link = Link()
        api_link.id = link.ID
        api_link.begin_node_id = link.BeginNodeID
        api_link.end_node_id = link.EndNodeID
        api_link.length = link.Length    

        return api_link, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_links():  # noqa: E501
    """List links

    List all links # noqa: E501


    :rtype: List[Link]
    """
    try:
        links = session.execute(
            select([lds.Link])
        )

        print(links)

        api_links = []
        for link, in links:
            api_link = Link()
            api_link.id = link.ID
            api_link.begin_node_id = link.BeginNodeID
            api_link.end_node_id = link.EndNodeID
            api_link.length = link.Length            
            api_links.append(api_link)        


        return api_links, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500
