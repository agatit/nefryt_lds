import os
import sys
from datetime import datetime, timedelta, timezone
import jwt
from starlette import status
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from api.routers.utils.security import SECRET_KEY, ALGORITHM


login_data1: dict = {'username': 'user1',
                     'password': 'abc'}
login_data2: dict = {'username': 'admin',
                     'password': 'xyz'}
datetime_now = datetime.now(timezone.utc)
token_data = {
    'iss': 'https://api.nefrytlds.local/',
    'sub': 'user',
    'nbf': datetime_now.timestamp(),
    'iat': datetime_now.timestamp(),
    'exp': (datetime_now + timedelta(hours=24)).timestamp(),
    'perms': ['confirm', 'refresh']
}

test_client = TestClient(app)


def test_auth_login_should_return_ok_response_code_and_correct_login_permissions_data_for_guest():
    response = test_client.post("/auth/login", json=login_data1)
    assert response.status_code == status.HTTP_200_OK
    login_permissions = response.json()
    assert login_permissions['username'] == login_data1['username']
    assert login_permissions['success']
    assert (datetime.fromisoformat(login_permissions['refreshTokenExpiration'].rstrip('Z')).replace(tzinfo=timezone.utc)
            - datetime.now(tz=timezone.utc) <= timedelta(hours=24))
    assert login_permissions['permissions'] == []


def test_auth_login_should_return_ok_response_code_and_correct_login_permissions_data_for_admin():
    response = test_client.post("/auth/login", json=login_data2)
    assert response.status_code == status.HTTP_200_OK
    login_permissions = response.json()
    assert login_permissions['username'] == login_data2['username']
    assert login_permissions['success']
    assert (datetime.fromisoformat(login_permissions['refreshTokenExpiration'].rstrip('Z')).replace(tzinfo=timezone.utc)
            - datetime.now(tz=timezone.utc) <= timedelta(hours=24))
    assert set(login_permissions['permissions']) == {'admin', 'confirm'}


def test_auth_login_should_return_ok_response_code_and_correct_tokens():
    response = test_client.post("/auth/login", json=login_data2)
    assert response.status_code == status.HTTP_200_OK
    token = jwt.decode(response.json()['token'], SECRET_KEY, algorithms=[ALGORITHM])
    assert token['sub'] == login_data2['username']
    assert set(token['perms']) == {'admin', 'confirm'}
    assert datetime.fromtimestamp(token['exp']) - datetime.now() <= timedelta(hours=1)
    refresh_token = jwt.decode(response.json()['refreshToken'], SECRET_KEY, algorithms=[ALGORITHM])
    assert refresh_token['sub'] == login_data2['username']
    assert set(refresh_token['perms']) == {'refresh', 'admin', 'confirm'}
    assert datetime.fromtimestamp(refresh_token['exp']) - datetime.now() <= timedelta(hours=24)


def test_auth_refresh_should_return_ok_response_code_and_correct_login_permissions_data():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_200_OK
    login_permissions = response.json()
    assert login_permissions['username'] == token_data['sub']
    assert login_permissions['success']
    assert (datetime.fromisoformat(login_permissions['refreshTokenExpiration'].rstrip('Z')).replace(tzinfo=timezone.utc)
            - datetime.now(tz=timezone.utc) <= timedelta(hours=24))
    assert set(login_permissions['permissions']) == set([perm for perm in token_data['perms'] if perm != 'refresh'])


def test_auth_refresh_should_return_ok_response_code_and_correct_tokens():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_200_OK
    token = jwt.decode(response.json()['token'], SECRET_KEY, algorithms=[ALGORITHM])
    assert token['sub'] == token_data['sub']
    assert set(token['perms']) == set([perm for perm in token_data['perms'] if perm != 'refresh'])
    assert datetime.fromtimestamp(token['exp']) - datetime.now() <= timedelta(hours=1)
    refresh_token = jwt.decode(response.json()['refreshToken'], SECRET_KEY, algorithms=[ALGORITHM])
    assert refresh_token['sub'] == token_data['sub']
    assert set(refresh_token['perms']) == set(token_data['perms'])
    assert datetime.fromtimestamp(refresh_token['exp']) - datetime.now() <= timedelta(hours=24)


def test_auth_refresh_should_return_bad_request_response_code_and_error_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bearer {encoded_token}1"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    error = response.json()
    assert error['code'] == status.HTTP_401_UNAUTHORIZED
    assert error['message'] == 'Invalid token'


def test_auth_refresh_should_return_unauthorized_response_code_when_header_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    header = {"Authorization": f"Bear {encoded_token}"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    header = {"Authorizations": f"Bearer {encoded_token}"}
    response = test_client.post("/auth/refresh", headers=header)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
