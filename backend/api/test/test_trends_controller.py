# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.trend import Trend  # noqa: E501
from api.models.trend_data import TrendData  # noqa: E501
from api.models.trend_param import TrendParam  # noqa: E501
from api.test import BaseTestCase


class TestTrendsController(BaseTestCase):
    """TrendsController integration test stubs"""

    def test_create_trend(self):
        """Test case for create_trend

        Create trend
        """
        trend = {
  "TrendGroupID" : 0,
  "TrendDefID" : 6,
  "ID" : 0,
  "Name" : "Name"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/trend',
            method='POST',
            headers=headers,
            data=json.dumps(trend),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_trend_by_id(self):
        """Test case for delete_trend_by_id

        Deletes trend
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trend/{trend_id}'.format(trend_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_trend_by_id(self):
        """Test case for get_trend_by_id

        Detail trend
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trend/{trend_id}'.format(trend_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_trend_data(self):
        """Test case for get_trend_data

        List trend data
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trend/{trend_id}/data/{start}/{end}/{resolution}'.format(trend_id=56, start=56, end=56, resolution=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_trend_param_by_id(self):
        """Test case for get_trend_param_by_id

        Gets trend param detail
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trend/{trend_id}/param/{param_id}'.format(trend_id=56, param_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_trend_params(self):
        """Test case for list_trend_params

        List trend params
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trend/{trend_id}/param'.format(trend_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_trends(self):
        """Test case for list_trends

        List trends
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/trend',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_trend(self):
        """Test case for update_trend

        Update trend
        """
        trend = {
  "TrendGroupID" : 0,
  "TrendDefID" : 6,
  "ID" : 0,
  "Name" : "Name"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/trend',
            method='PUT',
            headers=headers,
            data=json.dumps(trend),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_trend_param(self):
        """Test case for update_trend_param

        Update trend params
        """
        trend_param = {
  "TrendParamDefID" : 1,
  "Value" : "Value",
  "DataType" : "DataType",
  "TrendDefID" : 6,
  "TrendID" : 0,
  "Name" : "Name"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/trend/{trend_id}/param'.format(trend_id=56),
            method='PUT',
            headers=headers,
            data=json.dumps(trend_param),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
