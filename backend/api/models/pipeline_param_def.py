# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
import re
from api import util

import re  # noqa: E501

class PipelineParamDef(Model):
    """NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.
    """

    def __init__(self, id=None, pipeline_def_id=None, name=None, data_type=None):  # noqa: E501
        """PipelineParamDef - a model defined in OpenAPI

        :param id: The id of this PipelineParamDef.  # noqa: E501
        :type id: int
        :param pipeline_def_id: The pipeline_def_id of this PipelineParamDef.  # noqa: E501
        :type pipeline_def_id: int
        :param name: The name of this PipelineParamDef.  # noqa: E501
        :type name: str
        :param data_type: The data_type of this PipelineParamDef.  # noqa: E501
        :type data_type: str
        """
        self.openapi_types = {
            'id': int,
            'pipeline_def_id': int,
            'name': str,
            'data_type': str
        }

        self.attribute_map = {
            'id': 'ID',
            'pipeline_def_id': 'PipelineDefID',
            'name': 'Name',
            'data_type': 'DataType'
        }

        self._id = id
        self._pipeline_def_id = pipeline_def_id
        self._name = name
        self._data_type = data_type

    @classmethod
    def from_dict(cls, dikt) -> 'PipelineParamDef':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PipelineParamDef of this PipelineParamDef.  # noqa: E501
        :rtype: PipelineParamDef
        """
        return util.deserialize_model(dikt, cls)

    @property
    def id(self):
        """Gets the id of this PipelineParamDef.

        none  # noqa: E501

        :return: The id of this PipelineParamDef.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this PipelineParamDef.

        none  # noqa: E501

        :param id: The id of this PipelineParamDef.
        :type id: int
        """

        self._id = id

    @property
    def pipeline_def_id(self):
        """Gets the pipeline_def_id of this PipelineParamDef.

        none  # noqa: E501

        :return: The pipeline_def_id of this PipelineParamDef.
        :rtype: int
        """
        return self._pipeline_def_id

    @pipeline_def_id.setter
    def pipeline_def_id(self, pipeline_def_id):
        """Sets the pipeline_def_id of this PipelineParamDef.

        none  # noqa: E501

        :param pipeline_def_id: The pipeline_def_id of this PipelineParamDef.
        :type pipeline_def_id: int
        """

        self._pipeline_def_id = pipeline_def_id

    @property
    def name(self):
        """Gets the name of this PipelineParamDef.

        none  # noqa: E501

        :return: The name of this PipelineParamDef.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this PipelineParamDef.

        none  # noqa: E501

        :param name: The name of this PipelineParamDef.
        :type name: str
        """
        if name is not None and not re.search(r'^.{0,30}', name):  # noqa: E501
            raise ValueError("Invalid value for `name`, must be a follow pattern or equal to `/^.{0,30}/`")  # noqa: E501

        self._name = name

    @property
    def data_type(self):
        """Gets the data_type of this PipelineParamDef.

        none  # noqa: E501

        :return: The data_type of this PipelineParamDef.
        :rtype: str
        """
        return self._data_type

    @data_type.setter
    def data_type(self, data_type):
        """Sets the data_type of this PipelineParamDef.

        none  # noqa: E501

        :param data_type: The data_type of this PipelineParamDef.
        :type data_type: str
        """
        if data_type is not None and not re.search(r'^.{0,6}', data_type):  # noqa: E501
            raise ValueError("Invalid value for `data_type`, must be a follow pattern or equal to `/^.{0,6}/`")  # noqa: E501

        self._data_type = data_type
