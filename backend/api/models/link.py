# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api import util


class Link(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, begin_node_id=None, end_node_id=None, length=None):  # noqa: E501
        """Link - a model defined in OpenAPI

        :param id: The id of this Link.  # noqa: E501
        :type id: int
        :param begin_node_id: The begin_node_id of this Link.  # noqa: E501
        :type begin_node_id: int
        :param end_node_id: The end_node_id of this Link.  # noqa: E501
        :type end_node_id: int
        :param length: The length of this Link.  # noqa: E501
        :type length: float
        """
        self.openapi_types = {
            'id': int,
            'begin_node_id': int,
            'end_node_id': int,
            'length': float
        }

        self.attribute_map = {
            'id': 'ID',
            'begin_node_id': 'BeginNodeID',
            'end_node_id': 'EndNodeID',
            'length': 'Length'
        }

        self._id = id
        self._begin_node_id = begin_node_id
        self._end_node_id = end_node_id
        self._length = length

    @classmethod
    def from_dict(cls, dikt) -> 'Link':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Link of this Link.  # noqa: E501
        :rtype: Link
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this Link.

        none  # noqa: E501

        :return: The id of this Link.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Link.

        none  # noqa: E501

        :param id: The id of this Link.
        :type id: int
        """

        self._id = id

    @property
    def begin_node_id(self):
        """Gets the begin_node_id of this Link.

        none  # noqa: E501

        :return: The begin_node_id of this Link.
        :rtype: int
        """
        return self._begin_node_id

    @begin_node_id.setter
    def begin_node_id(self, begin_node_id):
        """Sets the begin_node_id of this Link.

        none  # noqa: E501

        :param begin_node_id: The begin_node_id of this Link.
        :type begin_node_id: int
        """

        self._begin_node_id = begin_node_id

    @property
    def end_node_id(self):
        """Gets the end_node_id of this Link.

        none  # noqa: E501

        :return: The end_node_id of this Link.
        :rtype: int
        """
        return self._end_node_id

    @end_node_id.setter
    def end_node_id(self, end_node_id):
        """Sets the end_node_id of this Link.

        none  # noqa: E501

        :param end_node_id: The end_node_id of this Link.
        :type end_node_id: int
        """

        self._end_node_id = end_node_id

    @property
    def length(self):
        """Gets the length of this Link.

        none  # noqa: E501

        :return: The length of this Link.
        :rtype: float
        """
        return self._length

    @length.setter
    def length(self, length):
        """Sets the length of this Link.

        none  # noqa: E501

        :param length: The length of this Link.
        :type length: float
        """

        self._length = length
