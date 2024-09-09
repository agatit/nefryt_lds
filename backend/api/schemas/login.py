from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, Field


class Login(BaseModel, OAuth2PasswordRequestForm):
    username: str = Field(min_length=1)
    password: str = Field(min_length=1)
    device_id: str | None = Field(None, min_length=1, alias='deviceId')
    device_name: str | None = Field(None, min_length=1, alias='deviceName')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
