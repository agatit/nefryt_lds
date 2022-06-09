# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.error import Error  # noqa: E501
from api.models.event import Event  # noqa: E501
from api.models.information import Information  # noqa: E501
from api.test import BaseTestCase


class TestEventsController(BaseTestCase):
    """EventsController integration test stubs"""

    def test_ack_event(self):
        """Test case for ack_event

        Acknowledges ack
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/event/{event_id}/ack'.format(event_id=56),
            method='POST',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_event_by_id(self):
        """Test case for get_event_by_id

        Gets detailed event
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/event/{event_id}'.format(event_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_events(self):
        """Test case for list_events

        List events
        """
        headers = { 
            'Accept': 'application/json',
        }
        response = self.client.open(
            '/event',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
