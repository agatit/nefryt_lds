import os
import sys
from unittest.mock import patch
from starlette import status
from starlette.testclient import TestClient
from conftest import test_client
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.routers.utils.security import get_user_token


def test_run_past_detector_should_return_no_content_response_code(test_client):
    module_params_dict = {'detection_periods': [90000, 100000, 888888, 999999]}
    with patch("api.routers.leak_detector.subprocess.Popen") as popen_mock:
        response = test_client.post("/leak_detector/run_past_detector", json=module_params_dict)
        popen_mock.assert_called_once()
        assert response.status_code == status.HTTP_204_NO_CONTENT
