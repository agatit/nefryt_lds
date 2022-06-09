# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.method_param import MethodParam  # noqa: E501
from api.test import BaseTestCase


class TestMethodsController(BaseTestCase):
    """MethodsController integration test stubs"""

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


if __name__ == '__main__':
    unittest.main()
