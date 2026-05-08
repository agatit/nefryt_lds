from pydantic import BaseModel, Field


class Login(BaseModel):
    username: str
    password: str
    deviceId: str | None = Field(None)
    deviceName: str | None = Field(None)
