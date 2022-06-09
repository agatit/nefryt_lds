# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.node import Node  # noqa: E501
from api.test import BaseTestCase


class TestNodesController(BaseTestCase):
    """NodesController integration test stubs"""

    def test_create_node(self):
        """Test case for create_node

        Create nodes
        """
        node = {
  "Type" : "Type",
  "EditorParams" : {
    "PosX" : 6,
    "PosY" : 1
  },
  "ID" : 0,
  "TrendID" : 0,
  "Name" : "Name"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/node',
            method='POST',
            headers=headers,
            data=json.dumps(node),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_node_by_id(self):
        """Test case for delete_node_by_id

        Deletes node
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/node/{node_id}'.format(node_id=56),
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_node_by_id(self):
        """Test case for get_node_by_id

        Gets node details
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/node/{node_id}'.format(node_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_nodes(self):
        """Test case for list_nodes

        List nodes
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/node',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_node(self):
        """Test case for update_node

        Updates nodes
        """
        node = {
  "Type" : "Type",
  "EditorParams" : {
    "PosX" : 6,
    "PosY" : 1
  },
  "ID" : 0,
  "TrendID" : 0,
  "Name" : "Name"
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/node',
            method='PUT',
            headers=headers,
            data=json.dumps(node),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
