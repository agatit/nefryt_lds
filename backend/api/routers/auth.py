from typing import Annotated
from fastapi import APIRouter, Body, Depends
from ..routers.security import prepare_login_permissions, get_refresh_token
from ..schemas import Login, LoginPermissions

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginPermissions)
async def auth_login(login_data: Annotated[Login, Body()]):
    # TODO: real check of credentials
    if login_data.username == "admin":
        permissions = ["admin", "confirm"]
    else:
        permissions = []
    success = True
    username = login_data.username

    return prepare_login_permissions(username, permissions, success)


@router.post("/refresh", response_model=LoginPermissions)
async def auth_refresh(token: Annotated[dict, Depends(get_refresh_token)]):
    permissions = token.get('perms')
    permissions.remove('refresh')
    success = True
    username = token.get('sub', 'guest')

    return prepare_login_permissions(username, permissions, success)
