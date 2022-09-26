# coding: utf-8

from __future__ import absolute_import
import unittest

from flask import json
from six import BytesIO

from api.models.error import Error  # noqa: E501
from api.models.unit import Unit  # noqa: E501
from api.test import BaseTestCase


class TestUnitsController(BaseTestCase):
    """UnitsController integration test stubs"""

    def test_get_unit_by_id(self):
        """Test case for get_unit_by_id

        Gets detailed unit
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/unit/{unit_id}'.format(unit_id=56),
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_list_units(self):
        """Test case for list_units

        List units
        """
        headers = { 
            'Accept': 'application/json',
            'Authorization': 'Bearer special-key',
        }
        response = self.client.open(
            '/unit',
            method='GET',
            headers=headers)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
