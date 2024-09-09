from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
import jwt


SECRET_KEY = "45bfa25ea5ae73f9f46909ac22e5ff72d51362129e210e3bc2c728957ee18230"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def generate_token(username: str, permissions: list[str], time: datetime, expiration_time: datetime) -> str:
    data = {
        'iss': 'https://api.nefrytlds.local/',
        'sub': username,
        'iat': time,
        'exp': expiration_time,
        'perms': permissions
    }
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def calculate_expiration_time(current_time: datetime, hours: int) -> datetime:
    return current_time + timedelta(hours=hours)


def get_user_permissions(encoded_token: Annotated[str, Depends(oauth2_scheme)]) -> list[str]:
    try:
        print('1')
        decoded_token = decode_token(encoded_token)
        print('3')
        return decoded_token.get('perms')
    except InvalidTokenError:
        print('2')
        return []


def decode_token(encoded_token: str) -> str:
    return jwt.decode(encoded_token, SECRET_KEY, algorithms=[ALGORITHM])


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return pwd_context.hash(password)
