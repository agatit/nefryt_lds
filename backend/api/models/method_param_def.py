# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
import re
from api import util

import re  # noqa: E501

class MethodParamDef(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, method_def_id=None, name=None, data_type=None):  # noqa: E501
        """MethodParamDef - a model defined in OpenAPI

        :param id: The id of this MethodParamDef.  # noqa: E501
        :type id: int
        :param method_def_id: The method_def_id of this MethodParamDef.  # noqa: E501
        :type method_def_id: int
        :param name: The name of this MethodParamDef.  # noqa: E501
        :type name: str
        :param data_type: The data_type of this MethodParamDef.  # noqa: E501
        :type data_type: str
        """
        self.openapi_types = {
            'id': int,
            'method_def_id': int,
            'name': str,
            'data_type': str
        }

        self.attribute_map = {
            'id': 'ID',
            'method_def_id': 'MethodDefID',
            'name': 'Name',
            'data_type': 'DataType'
        }

        self._id = id
        self._method_def_id = method_def_id
        self._name = name
        self._data_type = data_type

    @classmethod
    def from_dict(cls, dikt) -> 'MethodParamDef':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MethodParamDef of this MethodParamDef.  # noqa: E501
        :rtype: MethodParamDef
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this MethodParamDef.

        none  # noqa: E501

        :return: The id of this MethodParamDef.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MethodParamDef.

        none  # noqa: E501

        :param id: The id of this MethodParamDef.
        :type id: int
        """

        self._id = id

    @property
    def method_def_id(self):
        """Gets the method_def_id of this MethodParamDef.

        none  # noqa: E501

        :return: The method_def_id of this MethodParamDef.
        :rtype: int
        """
        return self._method_def_id

    @method_def_id.setter
    def method_def_id(self, method_def_id):
        """Sets the method_def_id of this MethodParamDef.

        none  # noqa: E501

        :param method_def_id: The method_def_id of this MethodParamDef.
        :type method_def_id: int
        """

        self._method_def_id = method_def_id

    @property
    def name(self):
        """Gets the name of this MethodParamDef.

        none  # noqa: E501

        :return: The name of this MethodParamDef.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MethodParamDef.

        none  # noqa: E501

        :param name: The name of this MethodParamDef.
        :type name: str
        """
        if name is not None and not re.search(r'^.{0,30}', name):  # noqa: E501
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/^.{0,30}/`")  # noqa: E501

        self._name = name

    @property
    def data_type(self):
        """Gets the data_type of this MethodParamDef.

        none  # noqa: E501

        :return: The data_type of this MethodParamDef.
        :rtype: str
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """Sets the data_type of this MethodParamDef.

        none  # noqa: E501

        :param data_type: The data_type of this MethodParamDef.
        :type data_type: str
        """
        if data_type is not None and not re.search(r'^.{0,6}', data_type):  # noqa: E501
            raise ValueError("Invalid value for `data_type`, must be a follow pattern or equal to `/^.{0,6}/`")  # noqa: E501

        self._data_type = data_type
