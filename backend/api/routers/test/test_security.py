import os
import sys
from datetime import datetime, timedelta, timezone
import jwt
import pytest
from fastapi import HTTPException
from jwt import InvalidSignatureError, InvalidTokenError
from starlette.testclient import TestClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))  # noqa: E402
from api import app
from api.routers.security import (SECRET_KEY, ALGORITHM, generate_token, calculate_expiration_time,
                                  get_user_permissions, get_user_token, decode_token, pwd_context,
                                  verify_password, hash_password)


login_data1: dict = {'username': 'user1',
                     'password': 'abc'}
login_data2: dict = {'username': 'admin',
                     'password': 'Kartofel_1410'}
token_data = {
    'iss': 'https://api.nefrytlds.local/',
    'sub': 'user',
    'iat': datetime.now(tz=timezone.utc).timestamp(),
    'exp': (datetime.now(tz=timezone.utc) + timedelta(hours=24)).timestamp(),
    'perms': ['confirm', 'admin']
}
password = 'abc'


test_client = TestClient(app)


def test_generate_token_should_return_encoded_token_with_correct_data():
    encoded_token = generate_token(token_data['sub'], token_data['perms'], token_data['iat'], token_data['exp'])
    token = jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])
    for key in token_data:
        assert token[key] == token_data[key]


def test_calculate_expiration_time_should_return_correct_time():
    expiration_time = calculate_expiration_time(datetime.fromtimestamp(token_data['iat']), 24)
    assert expiration_time.timestamp() == token_data['exp']


def test_get_user_permissions_should_return_correct_permissions():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    permissions = get_user_permissions(encoded_token)
    assert permissions == token_data['perms']


def test_get_user_permissions_should_return_empty_list_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    permissions = get_user_permissions(encoded_token+'1')
    assert permissions == []


def test_get_user_token_should_return_correct_token():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    token = get_user_token(encoded_token)
    for key in token_data:
        assert token[key] == token_data[key]


def test_get_user_token_should_raise_http_exception_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(HTTPException):
        get_user_token(encoded_token+'1')


def test_decode_token_should_return_correct_token():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    token = decode_token(encoded_token)
    for key in token_data:
        assert token[key] == token_data[key]


def test_decode_token_should_raise_invalid_signature_error_when_token_is_invalid():
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(InvalidSignatureError):
        decode_token(encoded_token+'1')


def test_decode_token_should_raise_invalid_token_error_when_token_is_expired():
    token_data['exp'] = (datetime.now(tz=timezone.utc) - timedelta(hours=24)).timestamp()
    encoded_token = jwt.encode(token_data, SECRET_KEY, ALGORITHM)
    with pytest.raises(InvalidTokenError):
        decode_token(encoded_token)


def test_verify_password_should_return_if_passwords_are_equal():
    hashed_password = pwd_context.hash(password)
    assert verify_password(password, hashed_password)
    assert not verify_password(password+'a', hashed_password)


def test_hash_password_should_return_correct_hash():
    hashed_password = hash_password(password)
    assert pwd_context.verify(password, hashed_password)
