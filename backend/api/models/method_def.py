# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
import re
from api import util

import re  # noqa: E501

class MethodDef(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, name=None):  # noqa: E501
        """MethodDef - a model defined in OpenAPI

        :param id: The id of this MethodDef.  # noqa: E501
        :type id: int
        :param name: The name of this MethodDef.  # noqa: E501
        :type name: str
        """
        self.openapi_types = {
            'id': int,
            'name': str
        }

        self.attribute_map = {
            'id': 'ID',
            'name': 'Name'
        }

        self._id = id
        self._name = name

    @classmethod
    def from_dict(cls, dikt) -> 'MethodDef':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MethodDef of this MethodDef.  # noqa: E501
        :rtype: MethodDef
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this MethodDef.

        none  # noqa: E501

        :return: The id of this MethodDef.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MethodDef.

        none  # noqa: E501

        :param id: The id of this MethodDef.
        :type id: int
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this MethodDef.

        none  # noqa: E501

        :return: The name of this MethodDef.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MethodDef.

        none  # noqa: E501

        :param name: The name of this MethodDef.
        :type name: str
        """
        if name is not None and not re.search(r'^.{0,30}', name):  # noqa: E501
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/^.{0,30}/`")  # noqa: E501

        self._name = name
