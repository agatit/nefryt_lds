# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.error import Error  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.models.link import Link  # noqa: E501
from api.test import BaseTestCase


class TestLinksController(BaseTestCase):
    """LinksController integration test stubs"""

    def test_create_link(self):
        """Test case for create_link

        Create links
        """
        link = {
  "BeginNodeID" : 0,
  "Length" : 1.4658129805029452,
  "ID" : 0,
  "EndNodeID" : 6
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/link',
            method='POST',
            headers=headers,
            data=json.dumps(link),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_link_by_id(self):
        """Test case for delete_link_by_id

        Deletes link
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/link/{link_id}',
            method='DELETE',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_link_by_id(self):
        """Test case for get_link_by_id

        Gets link details
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/link/{link_id}'.format(link_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_links(self):
        """Test case for list_links

        List links
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/link',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_link(self):
        """Test case for update_link

        Updates links
        """
        link = {
  "BeginNodeID" : 0,
  "Length" : 1.4658129805029452,
  "ID" : 0,
  "EndNodeID" : 6
}
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
        response = self.client.open(
            '/link/{link_id}',
            method='PUT',
            headers=headers,
            data=json.dumps(link),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
