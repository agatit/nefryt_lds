import copy
import os
import sys
from datetime import datetime, timedelta, timezone
import jwt
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidSignatureError, InvalidTokenError
from starlette.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api.app import app
from api.routers.security import (SECRET_KEY, ALGORITHM, generate_token, get_expiration_time,
                                  get_user_permissions, get_user_token, decode_token, pwd_context,
                                  verify_password, hash_password, is_refresh, get_refresh_token,
                                  prepare_login_permissions)

login_data1: dict = {'username': 'user1',
                     'password': 'abc'}
login_data2: dict = {'username': 'admin',
                     'password': 'xyz'}
datetime_now = datetime.now(timezone.utc)
token_data = {
    'iss': 'https://api.nefrytlds.local/',
    'sub': 'user',
    'nbf': int(datetime_now.timestamp()),
    'iat': int(datetime_now.timestamp()),
    'exp': int((datetime_now + timedelta(hours=24)).timestamp()),
    'perms': ['confirm', 'admin']
}
refresh_token_data = copy.deepcopy(token_data)
refresh_token_data['perms'] = ['confirm', 'refresh']
expired_token_data = copy.deepcopy(token_data)
expired_token_data['exp'] = int((datetime_now - timedelta(hours=24)).timestamp())
expired_refresh_token_data = copy.deepcopy(refresh_token_data)
expired_refresh_token_data['exp'] = int((datetime_now - timedelta(hours=24)).timestamp())
password = 'abc'

test_client = TestClient(app)


def test_generate_token_should_return_encoded_token_with_correct_data():
    encoded_token = generate_token(token_data['sub'], token_data['perms'],
                                   datetime.fromtimestamp(token_data['iat'], timezone.utc),
                                   datetime.fromtimestamp(token_data['exp'], timezone.utc))
    token = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
    for key in token_data:
        assert token[key] == token_data[key]


def test_get_expiration_time_should_return_correct_time():
    expiration_time = get_expiration_time(datetime.fromtimestamp(token_data['iat']), 24)
    assert expiration_time.timestamp() == token_data['exp']


def test_is_refresh_should_return_correct_value():
    result = is_refresh(token_data)
    assert result is False
    result = is_refresh(refresh_token_data)
    assert result is True


def test_get_user_permissions_should_return_correct_permissions():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    permissions = get_user_permissions(HTTPAuthorizationCredentials(credentials=encoded_token, scheme=''))
    assert set(permissions) == set(token_data['perms'])


def test_get_user_permissions_should_return_empty_list_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    permissions = get_user_permissions(HTTPAuthorizationCredentials(credentials=encoded_token + '1', scheme=''))
    assert permissions == []


def test_get_user_permissions_should_raise_http_exception_when_no_token_is_given():
    with pytest.raises(HTTPException):
        get_user_permissions(None)


def test_get_user_token_should_return_correct_token():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    token = get_user_token(HTTPAuthorizationCredentials(credentials=encoded_token, scheme=''))
    for key in token_data:
        assert token[key] == token_data[key]


def test_get_user_token_should_raise_http_exception_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(HTTPException):
        get_user_token(HTTPAuthorizationCredentials(credentials=encoded_token + '1', scheme=''))


def test_get_user_token_should_raise_http_exception_when_token_is_expired():
    encoded_token = jwt.encode(expired_token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(HTTPException):
        get_user_token(HTTPAuthorizationCredentials(credentials=encoded_token, scheme=''))


def test_get_user_token_should_raise_http_exception_when_token_is_refresh():
    encoded_token = jwt.encode(refresh_token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(HTTPException):
        get_user_token(HTTPAuthorizationCredentials(credentials=encoded_token, scheme=''))


def test_get_refresh_token_should_return_correct_token():
    encoded_token = jwt.encode(refresh_token_data, SECRET_KEY, ALGORITHM)
    token = get_refresh_token(HTTPAuthorizationCredentials(credentials=encoded_token, scheme=''))
    for key in token_data:
        assert token[key] == refresh_token_data[key]


def test_get_refresh_token_should_raise_http_exception_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(HTTPException):
        get_refresh_token(HTTPAuthorizationCredentials(credentials=encoded_token + '1', scheme=''))


def test_get_refresh_token_should_raise_http_exception_when_token_is_expired():
    encoded_token = jwt.encode(expired_refresh_token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(HTTPException):
        get_refresh_token(HTTPAuthorizationCredentials(credentials=encoded_token, scheme=''))


def test_get_refresh_token_should_raise_http_exception_when_token_is_not_refresh():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(HTTPException):
        get_refresh_token(HTTPAuthorizationCredentials(credentials=encoded_token, scheme=''))


def test_prepare_login_permissions_should_return_correct_data():
    success = False
    login_permissions = prepare_login_permissions(login_data1['username'], token_data['perms'], success)
    assert login_permissions.username == login_data1['username']
    assert login_permissions.success == success
    assert login_permissions.refresh_token_expiration - datetime.now(tz=timezone.utc) <= timedelta(hours=24)
    assert set(login_permissions.permissions) == set(token_data['perms'])


def test_decode_token_should_return_correct_token():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    token = decode_token(encoded_token)
    for key in token_data:
        assert token[key] == token_data[key]


def test_decode_token_should_raise_invalid_signature_error_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(InvalidSignatureError):
        decode_token(encoded_token + '1')


def test_decode_token_should_raise_invalid_token_error_when_token_is_expired():
    token_data['exp'] = int((datetime.now(tz=timezone.utc) - timedelta(hours=24)).timestamp())
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(InvalidTokenError):
        decode_token(encoded_token)


def test_verify_password_should_return_if_passwords_are_equal():
    hashed_password = pwd_context.hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password(password + 'a', hashed_password)


def test_hash_password_should_return_correct_hash():
    hashed_password = hash_password(password)
    assert pwd_context.verify(password, hashed_password)
