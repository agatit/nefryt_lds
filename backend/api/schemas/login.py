from pydantic import BaseModel, Field


class Login(BaseModel):
    username: str
    password: str
    device_id: str | None = Field(None, alias='deviceId')
    device_name: str | None = Field(None, alias='deviceName')
