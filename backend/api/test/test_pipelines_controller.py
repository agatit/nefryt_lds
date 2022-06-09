# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.method import Method  # noqa: E501
from api.models.method_param import MethodParam  # noqa: E501
from api.models.pipeline import Pipeline  # noqa: E501
from api.test import BaseTestCase


class TestPipelinesController(BaseTestCase):
    """PipelinesController integration test stubs"""

    def test_create_method(self):
        """Test case for create_method

        Creates pipelnie method
        """
        method = {
  "PipelineID" : 0,
  "MethodDefID" : 0,
  "ID" : 0,
  "Name" : "Arthur Dent"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/pipeline/{pipeline_id}/method'.format(pipeline_id=56),
            method='POST',
            headers=headers,
            data=json.dumps(method),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_pipeline(self):
        """Test case for create_pipeline

        Create pipelnie
        """
        pipeline = {
  "EditorParams" : {
    "AreaWidthDivision" : 5,
    "AreaHeightDivision" : 5,
    "AreaWidth" : 6,
    "SIUnitID" : 2,
    "ID" : 0,
    "AreaHeight" : 1
  },
  "ID" : 0,
  "BeginPos" : 0.8008281904610115,
  "Name" : "Name"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/pipeline',
            method='POST',
            headers=headers,
            data=json.dumps(pipeline),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_pipeline_by_id(self):
        """Test case for delete_pipeline_by_id

        Deletes pipeline
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pipeline/{pipeline_id}'.format(pipeline_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_pipeline_by_id(self):
        """Test case for get_pipeline_by_id

        Gets pipeline details
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pipeline/{pipeline_id}'.format(pipeline_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_method_params(self):
        """Test case for list_method_params

        List pipelnie method params
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pipeline/{pipeline_id}/method/{method_id}/param'.format(pipeline_id=56, method_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_methods(self):
        """Test case for list_methods

        List pipelnie methods
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pipeline/{pipeline_id}/method'.format(pipeline_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_pipelines(self):
        """Test case for list_pipelines

        List pipelnies
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/pipeline',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_method(self):
        """Test case for update_method

        Updates pipelnie method
        """
        method = {
  "PipelineID" : 0,
  "MethodDefID" : 0,
  "ID" : 0,
  "Name" : "Arthur Dent"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/pipeline/{pipeline_id}/method'.format(pipeline_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(method),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_method_params(self):
        """Test case for update_method_params

        Put pipelnie method params
        """
        method_param = {
  "MethodID" : 0,
  "Value" : "Value",
  "PipelineID" : 0,
  "DataType" : "DataType",
  "MethodParamDefID" : 0,
  "Name" : "Name"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/pipeline/{pipeline_id}/method/{method_id}/param'.format(pipeline_id=56, method_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(method_param),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_pipeline(self):
        """Test case for update_pipeline

        Updates pipeline
        """
        pipeline = {
  "EditorParams" : {
    "AreaWidthDivision" : 5,
    "AreaHeightDivision" : 5,
    "AreaWidth" : 6,
    "SIUnitID" : 2,
    "ID" : 0,
    "AreaHeight" : 1
  },
  "ID" : 0,
  "BeginPos" : 0.8008281904610115,
  "Name" : "Name"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/pipeline',
            method='PUT',
            headers=headers,
            data=json.dumps(pipeline),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
