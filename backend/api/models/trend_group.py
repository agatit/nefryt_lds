# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
import re
from api import util

import re  # noqa: E501

class TrendGroup(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None, analisis_only=None):  # noqa: E501
        """TrendGroup - a model defined in OpenAPI

        :param id: The id of this TrendGroup.  # noqa: E501
        :type id: int
        :param name: The name of this TrendGroup.  # noqa: E501
        :type name: str
        :param analisis_only: The analisis_only of this TrendGroup.  # noqa: E501
        :type analisis_only: bool
        """
        self.openapi_types = {
            'id': int,
            'name': str,
            'analisis_only': bool
        }

        self.attribute_map = {
            'id': 'ID',
            'name': 'Name',
            'analisis_only': 'AnalisisOnly'
        }

        self._id = id
        self._name = name
        self._analisis_only = analisis_only

    @classmethod
    def from_dict(cls, dikt) -> 'TrendGroup':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TrendGroup of this TrendGroup.  # noqa: E501
        :rtype: TrendGroup
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this TrendGroup.

        none  # noqa: E501

        :return: The id of this TrendGroup.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this TrendGroup.

        none  # noqa: E501

        :param id: The id of this TrendGroup.
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this TrendGroup.

        none  # noqa: E501

        :return: The name of this TrendGroup.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this TrendGroup.

        none  # noqa: E501

        :param name: The name of this TrendGroup.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501
        if name is not None and not re.search(r'^.{0,100}', name):  # noqa: E501
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/^.{0,100}/`")  # noqa: E501

        self._name = name

    @property
    def analisis_only(self):
        """Gets the analisis_only of this TrendGroup.

        none  # noqa: E501

        :return: The analisis_only of this TrendGroup.
        :rtype: bool
        """
        return self._analisis_only

    @analisis_only.setter
    def analisis_only(self, analisis_only):
        """Sets the analisis_only of this TrendGroup.

        none  # noqa: E501

        :param analisis_only: The analisis_only of this TrendGroup.
        :type analisis_only: bool
        """
        if analisis_only is None:
            raise ValueError("Invalid value for `analisis_only`, must not be `None`")  # noqa: E501

        self._analisis_only = analisis_only
