# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.inline_object import InlineObject  # noqa: E501
from api.models.inline_response200 import InlineResponse200  # noqa: E501
from api.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_post_auth_login(self):
        """Test case for post_auth_login

        Application Login
        """
        inline_object = api.InlineObject()
        headers = { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'x_api_key': 'x_api_key_example',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/auth/login',
            method='POST',
            headers=headers,
            data=json.dumps(inline_object),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
