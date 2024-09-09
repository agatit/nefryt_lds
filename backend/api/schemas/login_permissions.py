from datetime import datetime

from pydantic import BaseModel, Field


class LoginPermissions(BaseModel):
    username: str | None = Field(None, min_length=1)
    success: bool | None = None
    token: str = Field(min_length=1)
    refresh_token: str = Field(min_length=1, alias='refreshToken')
    refresh_token_expiration: datetime = Field(alias='refreshTokenExpiration')
    permissions: list[str] | None = None
