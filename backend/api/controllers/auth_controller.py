import connexion
import six

from api.models.login import Login  # noqa: E501
from api.models.login_permissions import LoginPermissions  # noqa: E501
from api import util

from .security_controller import generate_token, decode_token, get_secret


def auth_login(login=None):  # noqa: E501
    """Application Login

     # noqa: E501

    :param login: 
    :type login: dict | bytes

    :rtype: LoginPermissions
    """
    if connexion.request.is_json:
        login: Login = Login.from_dict(connexion.request.get_json())  # noqa: E501

    permissions = []
    success = False
    username = "guest"

    if login.username == "admin" and login.password == "Kartofel_1410":
        permissions = ["admin", "confirm"]
        success = True
        username = login.username

    token, expiration_time  = generate_token(username, permissions, hours=1)
    refresh_token, _  = generate_token(username, permissions, hours=24)
    
    return LoginPermissions(
        username=username,
        success=success,
        token=token,
        refresh_token=refresh_token,
        refresh_token_expiration=expiration_time,
        permissions=permissions
    )


def auth_refresh(token_info={}):  # noqa: E501
    """Application Login

     # noqa: E501


    :rtype: LoginPermissions
    """
    if connexion.request.is_json:
        login: Login = Login.from_dict(connexion.request.get_json())  # noqa: E501

    permissions = token_info.get('perms',[])
    success = True
    username = token_info.get('sub','')

    token, expiration_time  = generate_token(username, permissions, hours=1)
    refresh_token, _  = generate_token(username, permissions, hours=24)
    
    return LoginPermissions(
        username=username,
        success=success,
        token=token,
        refresh_token=refresh_token,
        refresh_token_expiration=expiration_time,
        permissions=permissions
    )
