# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api.models.editor_node import EditorNode
import re
from api import util

from api.models.editor_node import EditorNode  # noqa: E501
import re  # noqa: E501

class Node(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, type=None, trend_id=None, name=None, editor_params=None):  # noqa: E501
        """Node - a model defined in OpenAPI

        :param id: The id of this Node.  # noqa: E501
        :type id: int
        :param type: The type of this Node.  # noqa: E501
        :type type: str
        :param trend_id: The trend_id of this Node.  # noqa: E501
        :type trend_id: int
        :param name: The name of this Node.  # noqa: E501
        :type name: str
        :param editor_params: The editor_params of this Node.  # noqa: E501
        :type editor_params: EditorNode
        """
        self.openapi_types = {
            'id': int,
            'type': str,
            'trend_id': int,
            'name': str,
            'editor_params': EditorNode
        }

        self.attribute_map = {
            'id': 'ID',
            'type': 'Type',
            'trend_id': 'TrendID',
            'name': 'Name',
            'editor_params': 'EditorParams'
        }

        self._id = id
        self._type = type
        self._trend_id = trend_id
        self._name = name
        self._editor_params = editor_params

    @classmethod
    def from_dict(cls, dikt) -> 'Node':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Node of this Node.  # noqa: E501
        :rtype: Node
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Node.

        none  # noqa: E501

        :return: The id of this Node.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Node.

        none  # noqa: E501

        :param id: The id of this Node.
        :type id: int
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def type(self):
        """Gets the type of this Node.

        none  # noqa: E501

        :return: The type of this Node.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Node.

        none  # noqa: E501

        :param type: The type of this Node.
        :type type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        if type is not None and not re.search(r'^.{0,6}', type):  # noqa: E501
            raise ValueError("Invalid value for `type`, must be a follow pattern or equal to `/^.{0,6}/`")  # noqa: E501

        self._type = type

    @property
    def trend_id(self):
        """Gets the trend_id of this Node.

        none  # noqa: E501

        :return: The trend_id of this Node.
        :rtype: int
        """
        return self._trend_id

    @trend_id.setter
    def trend_id(self, trend_id):
        """Sets the trend_id of this Node.

        none  # noqa: E501

        :param trend_id: The trend_id of this Node.
        :type trend_id: int
        """

        self._trend_id = trend_id

    @property
    def name(self):
        """Gets the name of this Node.

        none  # noqa: E501

        :return: The name of this Node.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Node.

        none  # noqa: E501

        :param name: The name of this Node.
        :type name: str
        """
        if name is not None and not re.search(r'^.{0,50}', name):  # noqa: E501
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/^.{0,50}/`")  # noqa: E501

        self._name = name

    @property
    def editor_params(self):
        """Gets the editor_params of this Node.


        :return: The editor_params of this Node.
        :rtype: EditorNode
        """
        return self._editor_params

    @editor_params.setter
    def editor_params(self, editor_params):
        """Sets the editor_params of this Node.


        :param editor_params: The editor_params of this Node.
        :type editor_params: EditorNode
        """

        self._editor_params = editor_params
