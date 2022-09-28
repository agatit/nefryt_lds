from ast import stmt
import connexion
import six

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.unit import Unit  # noqa: E501
from api import util

from odata_query.sqlalchemy import apply_odata_query
from sqlalchemy import select, delete
from ..db import session
from database.models import lds
from .security_controller import check_permissions


def create_unit(unit=None, token_info={}):  # noqa: E501
    """Create units

    Create a units # noqa: E501

    :param unit: 
    :type unit: dict | bytes

    :rtype: Information
    """

    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_unit = Unit.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_unit = lds.Unit()
        db_unit.ID = api_unit.id
        db_unit.Name = api_unit.name
        db_unit.Symbol = api_unit.symbol
        db_unit.BaseID = api_unit.base_id
        db_unit.Multiplier = api_unit.multiplier
        session.add(db_unit)
        
        session.commit()

        return get_unit_by_id(db_unit.ID)

    except Exception as e:
        error: Error = Error(message=str(e), code=500)
        return error, 500        

def update_unit(unit_id, unit=None, token_info={}):  # noqa: E501
    """Create units

    Create a units # noqa: E501

    :param unit: 
    :type unit: dict | bytes

    :rtype: Information
    """

    try:
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403

        if connexion.request.is_json:
            api_unit = Unit.from_dict(connexion.request.get_json())  # noqa: E501
        else:
            return Error(message="Expected a JSON request", code=400), 400

        db_unit = session.get(lds.Unit, unit_id)
        if db_unit is None:
            return Error(message="Not Found", code=404), 404

        db_unit.Name = api_unit.name
        db_unit.Symbol = api_unit.symbol
        db_unit.BaseID = api_unit.base_id
        db_unit.Multiplier = api_unit.multiplier
        session.add(db_unit)

        session.commit()

        return get_unit_by_id(db_unit.ID)

    except Exception as e:
        return Error(message=str(e), code=500), 500  

def delete_unit_by_id(unit_id, token_info):  # noqa: E501
    """Detail unit

    Delete specific unit # noqa: E501

    :param unit_id: The id of the unit to retrieve
    :type unit_id: int

    :rtype: Information
    """
    try:     
        if not check_permissions(token_info, ['admin']):
            return Error(message="Forbidden", code=403), 403        

        db_unit = session.get(lds.Unit, unit_id)
        if db_unit is None:
            return Error(message="Not Found", code=404), 404
        session.delete(db_unit)
        session.commit()

        return Information(message="Success", status=200), 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def get_unit_by_id(unit_id):  # noqa: E501
    """Detail unit

    Info for specific unit # noqa: E501

    :param unit_id: The id of the unit to retrieve
    :type unit_id: int

    :rtype: Unit
    """
    try:
        db_unit: lds.Unit = session.get(lds.Unit, unit_id)
        if db_unit is None:
            return Error(message="Not Found", code=404), 404
        api_unit = Unit()
        if db_unit.ID is not None:
            api_unit.id = db_unit.ID.strip()
        api_unit.name = db_unit.Name
        api_unit.symbol = db_unit.Symbol
        if db_unit.BaseID is not None:
            api_unit.base_id = db_unit.BaseID.strip()
        api_unit.multiplier = db_unit.Multiplier

        return api_unit, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500


def list_units(token_info, filter=None, filter_=None):  # noqa: E501
    """List units

    List all units # noqa: E501


    :rtype: List[Unit]
    """
    try:
        stmt = select([lds.Unit])
        if filter_ is not None:
            stmt = apply_odata_query(stmt, filter_)        
        db_units = session.execute(stmt)

        api_units = []
        for db_unit, in db_units:
            api_unit = Unit()
            if db_unit.ID is not None:
                api_unit.id = db_unit.ID.strip()
            api_unit.name = db_unit.Name
            api_unit.symbol = db_unit.Symbol
            if db_unit.BaseID is not None:
                api_unit.base_id = db_unit.BaseID.strip()
            api_unit.multiplier = db_unit.Multiplier           
            api_units.append(api_unit)        

        return api_units, 200

    except Exception as e:
        return Error(message=str(e), code=500), 500
