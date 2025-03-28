from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import InvalidTokenError, InvalidSignatureError, ExpiredSignatureError
import jwt
from starlette import status
from ..schemas import LoginPermissions

SECRET_KEY = "45bfa25ea5ae73f9f46909ac22e5ff72d51362129e210e3bc2c728957ee18230"
ALGORITHM = "HS256"
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer(auto_error=False)
_iss = 'https://api.nefrytlds.local/'


def generate_token(username: str, permissions: list[str], time: datetime, expiration_time: datetime) -> str:
    data = {
        'iss': _iss,
        'sub': username,
        'nbf': time,
        'iat': time,
        'exp': expiration_time,
        'perms': permissions
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_expiration_time(current_time: datetime, hours: int) -> datetime:
    return current_time + timedelta(hours=hours)


def is_refresh(token: str) -> bool:
    permissions = token.get('perms', [])
    return 'refresh' in permissions


def get_user_permissions(user_credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> list[str]:
    if user_credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No token given')
    try:
        decoded_token = decode_token(user_credentials.credentials)
        return decoded_token.get('perms')
    except (InvalidTokenError, InvalidSignatureError):
        return []


def get_user_token(user_credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> str:
    if user_credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No token given or is in wrong format')
    try:
        decoded_token = decode_token(user_credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    except (InvalidTokenError, InvalidSignatureError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    if is_refresh(decoded_token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token has refresh permissions')
    return decoded_token


def get_refresh_token(user_credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> str:
    if user_credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='No token given or is in wrong format')
    try:
        decoded_token = decode_token(user_credentials.credentials)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token expired')
    except (InvalidTokenError, InvalidSignatureError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    if not is_refresh(decoded_token):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Token does not contain refresh permissions')
    return decoded_token


def decode_token(encoded_token: str) -> str:
    return jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])


def prepare_login_permissions(username: str, permissions: list[str], success: bool) -> LoginPermissions:
    current_time = datetime.now(tz=timezone.utc)
    expiration_time_token = get_expiration_time(hours=1, current_time=current_time)
    expiration_time_refresh_token = get_expiration_time(hours=24, current_time=current_time)

    token = generate_token(username, permissions, current_time, expiration_time_token)
    refresh_token = generate_token(username, permissions + ['refresh'], current_time, expiration_time_refresh_token)

    login_permissions = {
        'username': username,
        'success': success,
        'token': token,
        'refreshToken': refresh_token,
        'refreshTokenExpiration': expiration_time_refresh_token,
        'permissions': permissions
    }
    return LoginPermissions(**login_permissions)

# def verify_password(plain_password: str, hashed_password: str):
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# def hash_password(password: str):
#     return pwd_context.hash(password)
