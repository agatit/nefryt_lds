from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends
from jwt import InvalidTokenError
from starlette import status
from starlette.responses import JSONResponse
from ..routers.security import calculate_expiration_time, generate_token, verify_password, hash_password, \
    get_user_token
from ..schemas import Login, LoginPermissions, Error

router = APIRouter(prefix="/auth", tags=["auth"])


# tabela z kontami
# dodawanie kont
# deviceId i deviceName w polu login
# czas wygaśnięcia token refresha
# @router.post("/login")
# async def auth_login(username: Annotated[str, Form], password: Annotated[str, Form],
#                      device_id: Annotated[str | None, Form] = None, device_name: Annotated[str | None, Form] = None):
#     login_data = Login(username=username, password=password, deviceId=device_id, deviceName=device_name)
#     permissions = []
#     success = False
#     username = "guest"
#
#     if login_data.username == "admin" and verify_password(login_data.password, hash_password("Kartofel_1410")):
#         permissions = ["admin", "confirm"]
#         success = True
#         username = login_data.username
#
#     return prepare_login_permissions(username, permissions, success)


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
    try:
        permissions = token.get('perms', [])
        success = True
        username = token.get('sub', 'guest')
        return prepare_login_permissions(username, permissions, success)
    except InvalidTokenError:
        error = Error(code=status.HTTP_400_BAD_REQUEST, message='Token is invalid')
        return JSONResponse(content=error.model_dump(), status_code=status.HTTP_400_BAD_REQUEST)


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
