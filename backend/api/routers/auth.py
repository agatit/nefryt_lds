from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from jwt import InvalidTokenError, InvalidSignatureError
from starlette import status
from starlette.responses import JSONResponse
from ..routers.security import calculate_expiration_time, generate_token, verify_password, hash_password, \
    get_user_token
from ..schemas import Login, LoginPermissions, Error

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def auth_login(login_data: Annotated[Login, Depends()]):
    permissions = []
    success = False
    username = "guest"

    if login_data.username == "admin" and verify_password(login_data.password, hash_password("Kartofel_1410")):
        permissions = ["admin", "confirm"]
        success = True
        username = login_data.username

    return prepare_login_permissions(username, permissions, success)


@router.post("/refresh")
async def auth_refresh(token: Annotated[str, Depends(get_user_token)]):
    permissions = token.get('perms', [])
    success = True
    username = token.get('sub', 'guest')
    return prepare_login_permissions(username, permissions, success)


def prepare_login_permissions(username: str, permissions: list[str], success: bool) -> LoginPermissions:
    current_time = datetime.now(tz=timezone.utc)
    expiration_time_token = calculate_expiration_time(hours=1, current_time=current_time)
    expiration_time_refresh_token = calculate_expiration_time(hours=24, current_time=current_time)

    token = generate_token(username, permissions, current_time, expiration_time_token)
    refresh_token = generate_token(username, permissions, current_time, expiration_time_refresh_token)

    login_permissions = {
        'username': username,
        'success': success,
        'token': token,
        'refreshToken': refresh_token,
        'refreshTokenExpiration': expiration_time_refresh_token,
        'permissions': permissions
    }
    return LoginPermissions(**login_permissions)
