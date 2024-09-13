import os
import sys
from datetime import datetime, timedelta, timezone
import jwt
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api import app
from api.routers.security import SECRET_KEY, ALGORITHM


login_data1: dict = {'username': 'user1',
                     'password': 'abc'}
login_data2: dict = {'username': 'admin',
                     'password': 'Kartofel_1410'}
token_data = {
    'iss': 'https://api.nefrytlds.local/',
    'sub': 'user',
    'iat': datetime.now(tz=timezone.utc),
    'exp': datetime.now(tz=timezone.utc) + timedelta(hours=24),
    'perms': ['confirm']
}

test_client = TestClient(app)


def test_auth_login_should_return_ok_response_code_and_correct_login_permissions_data_for_guest():
    response = test_client.post("/auth/login", data=login_data1)
    assert response.status_code == status.HTTP_200_OK
    login_permissions = response.json()
    assert login_permissions['username'] == 'guest'
    assert not login_permissions['success']
    assert (timedelta(hours=23, minutes=59) <
            datetime.fromisoformat(login_permissions['refreshTokenExpiration'].rstrip('Z'))
            .replace(tzinfo=timezone.utc) - datetime.now(tz=timezone.utc) < timedelta(hours=24))
    assert response.json()['permissions'] == []


def test_auth_login_should_return_ok_response_code_and_correct_login_permissions_data_for_admin():
    response = test_client.post("/auth/login", data=login_data2)
    assert response.status_code == status.HTTP_200_OK
    login_permissions = response.json()
    assert login_permissions['username'] == 'admin'
    assert login_permissions['success']
    assert (timedelta(hours=23, minutes=59) <
            datetime.fromisoformat(login_permissions['refreshTokenExpiration'].rstrip('Z'))
            .replace(tzinfo=timezone.utc) - datetime.now(tz=timezone.utc) < timedelta(hours=24))
    assert response.json()['permissions'] == ['admin', 'confirm']


def test_auth_login_should_return_ok_response_code_and_correct_tokens():
    response = test_client.post("/auth/login", data=login_data2)
    assert response.status_code == status.HTTP_200_OK
    token = jwt.decode(response.json()['token'], SECRET_KEY, algorithms=[ALGORITHM])
    assert token['sub'] == 'admin'
    assert token['perms'] == ['admin', 'confirm']
    assert (timedelta(minutes=59) <
            datetime.fromtimestamp(token['exp']) - datetime.now() < timedelta(hours=1))
    refresh_token = jwt.decode(response.json()['refreshToken'], SECRET_KEY, algorithms=[ALGORITHM])
    assert refresh_token['sub'] == 'admin'
    assert refresh_token['perms'] == ['admin', 'confirm']
    assert (timedelta(hours=23, minutes=59) <
            datetime.fromtimestamp(refresh_token['exp']) - datetime.now() < timedelta(hours=24))


def test_auto_refresh_should_return_ok_response_code_and_correct_login_permissions_data():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_200_OK
    login_permissions = response.json()
    assert login_permissions['username'] == 'user'
    assert login_permissions['success']
    assert (timedelta(hours=23, minutes=59) <
            datetime.fromisoformat(login_permissions['refreshTokenExpiration'].rstrip('Z'))
            .replace(tzinfo=timezone.utc) - datetime.now(tz=timezone.utc) < timedelta(hours=24))
    assert response.json()['permissions'] == ['confirm']


def test_auto_refresh_should_return_ok_response_code_and_correct_tokens():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_200_OK
    token = jwt.decode(response.json()['token'], SECRET_KEY, algorithms=[ALGORITHM])
    assert token['sub'] == 'user'
    assert token['perms'] == ['confirm']
    assert (timedelta(minutes=59) <
            datetime.fromtimestamp(token['exp']) - datetime.now() < timedelta(hours=1))
    refresh_token = jwt.decode(response.json()['refreshToken'], SECRET_KEY, algorithms=[ALGORITHM])
    assert refresh_token['sub'] == 'user'
    assert refresh_token['perms'] == ['confirm']
    assert (timedelta(hours=23, minutes=59) <
            datetime.fromtimestamp(refresh_token['exp']) - datetime.now() < timedelta(hours=24))


def test_auto_refresh_should_return_bad_request_response_code_and_error_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}1"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    error = response.json()
    assert error['code'] == status.HTTP_400_BAD_REQUEST
    assert error['message'] == 'Token is invalid'


def test_auto_refresh_should_return_unauthorized_response_code_when_header_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bear {encoded_token}"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    header = {"Authorizations": f"Bearer {encoded_token}"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
