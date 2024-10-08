# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api import util


class PipelineNode(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, node_id=None, first=None):  # noqa: E501
        """PipelineNode - a model defined in OpenAPI

        :param id: The id of this PipelineNode.  # noqa: E501
        :type id: int
        :param node_id: The node_id of this PipelineNode.  # noqa: E501
        :type node_id: int
        :param first: The first of this PipelineNode.  # noqa: E501
        :type first: bool
        """
        self.openapi_types = {
            'id': int,
            'node_id': int,
            'first': bool
        }

        self.attribute_map = {
            'id': 'ID',
            'node_id': 'NodeID',
            'first': 'First'
        }

        self._id = id
        self._node_id = node_id
        self._first = first

    @classmethod
    def from_dict(cls, dikt) -> 'PipelineNode':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PipelineNode of this PipelineNode.  # noqa: E501
        :rtype: PipelineNode
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this PipelineNode.

        none  # noqa: E501

        :return: The id of this PipelineNode.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PipelineNode.

        none  # noqa: E501

        :param id: The id of this PipelineNode.
        :type id: int
        """

        self._id = id

    @property
    def node_id(self):
        """Gets the node_id of this PipelineNode.

        none  # noqa: E501

        :return: The node_id of this PipelineNode.
        :rtype: int
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id):
        """Sets the node_id of this PipelineNode.

        none  # noqa: E501

        :param node_id: The node_id of this PipelineNode.
        :type node_id: int
        """
        if node_id is None:
            raise ValueError("Invalid value for `node_id`, must not be `None`")  # noqa: E501

        self._node_id = node_id

    @property
    def first(self):
        """Gets the first of this PipelineNode.

        none  # noqa: E501

        :return: The first of this PipelineNode.
        :rtype: bool
        """
        return self._first

    @first.setter
    def first(self, first):
        """Sets the first of this PipelineNode.

        none  # noqa: E501

        :param first: The first of this PipelineNode.
        :type first: bool
        """

        self._first = first
