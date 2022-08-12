import connexion
from typing import List
import time
from datetime import datetime, timezone, timedelta

from api.models.unauthorized import Unauthorized  # noqa: E501

import jwt

JWT_SECRET = "onyks$usONYKS4US"
JWT_ALGORITHM = "HS256"


def check_permissions(token_info, permissions):
    return any(p in token_info.get('perms',[]) for p in permissions)


def generate_token(user_id, permissions, hours):
    time = datetime.now(tz=timezone.utc)
    expiration_time = datetime.now(tz=timezone.utc) + timedelta(hours=hours)
    message = {
        'iss': 'https://api.nefrytlds.local/',
        'sub': user_id,
        'iat': time,
        'exp': expiration_time,
        'perms': permissions
    }
    return jwt.encode(message, JWT_SECRET, algorithm=JWT_ALGORITHM), expiration_time


def decode_token(token):
    try:
        token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return token
    except jwt.DecodeError as e:
        raise jwt.DecodeError("Token is invalid") from e


def get_secret(user, token_info) -> str:
    return """
    You are user_id {user} and the secret is 'onyks$us'.
    Decoded token claims: {token_info}.
    """.format(
        user=user, token_info=token_info
    )



    #    return Unauthorized(error="Unauthorized", status=401, timestamp=time.time(), path=connexion.request.path)

