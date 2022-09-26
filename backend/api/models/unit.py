# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api import util


class Unit(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, symbol=None, base_id=None, multiplier=None):  # noqa: E501
        """Unit - a model defined in OpenAPI

        :param id: The id of this Unit.  # noqa: E501
        :type id: str
        :param name: The name of this Unit.  # noqa: E501
        :type name: str
        :param symbol: The symbol of this Unit.  # noqa: E501
        :type symbol: str
        :param base_id: The base_id of this Unit.  # noqa: E501
        :type base_id: str
        :param multiplier: The multiplier of this Unit.  # noqa: E501
        :type multiplier: float
        """
        self.openapi_types = {
            'id': str,
            'name': str,
            'symbol': str,
            'base_id': str,
            'multiplier': float
        }

        self.attribute_map = {
            'id': 'ID',
            'name': 'Name',
            'symbol': 'Symbol',
            'base_id': 'BaseID',
            'multiplier': 'Multiplier'
        }

        self._id = id
        self._name = name
        self._symbol = symbol
        self._base_id = base_id
        self._multiplier = multiplier

    @classmethod
    def from_dict(cls, dikt) -> 'Unit':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Unit of this Unit.  # noqa: E501
        :rtype: Unit
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Unit.


        :return: The id of this Unit.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Unit.


        :param id: The id of this Unit.
        :type id: str
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this Unit.


        :return: The name of this Unit.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Unit.


        :param name: The name of this Unit.
        :type name: str
        """

        self._name = name

    @property
    def symbol(self):
        """Gets the symbol of this Unit.


        :return: The symbol of this Unit.
        :rtype: str
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """Sets the symbol of this Unit.


        :param symbol: The symbol of this Unit.
        :type symbol: str
        """

        self._symbol = symbol

    @property
    def base_id(self):
        """Gets the base_id of this Unit.


        :return: The base_id of this Unit.
        :rtype: str
        """
        return self._base_id

    @base_id.setter
    def base_id(self, base_id):
        """Sets the base_id of this Unit.


        :param base_id: The base_id of this Unit.
        :type base_id: str
        """

        self._base_id = base_id

    @property
    def multiplier(self):
        """Gets the multiplier of this Unit.


        :return: The multiplier of this Unit.
        :rtype: float
        """
        return self._multiplier

    @multiplier.setter
    def multiplier(self, multiplier):
        """Sets the multiplier of this Unit.


        :param multiplier: The multiplier of this Unit.
        :type multiplier: float
        """

        self._multiplier = multiplier
