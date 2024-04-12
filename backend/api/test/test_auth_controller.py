# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.login import Login  # noqa: E501
from api.models.login_permissions import LoginPermissions  # noqa: E501
from api.test import BaseTestCase


class TestAuthController(BaseTestCase):
    """AuthController integration test stubs"""

    def test_auth_login(self):
        """Test case for auth_login

        Application Login
        """
        login_permissions = {
  "refreshTokenExpiration" : "refreshTokenExpiration",
  "organisationName" : "organisationName",
  "organisationId" : "organisationId",
  "permissions" : [ {
    "key" : "{}"
  }, {
    "key" : "{}"
  } ],
  "userId" : "userId",
  "username" : "username",
  "token" : "token",
  "refreshToken" : "refreshToken"
}
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
            data=json.dumps(login_permissions),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
