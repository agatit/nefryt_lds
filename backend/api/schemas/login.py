from typing import Annotated
from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm


class Login(OAuth2PasswordRequestForm):
    def __init__(self, username: Annotated[str, Form()], password: Annotated[str, Form()],
                 device_id: Annotated[str | None, Form()] = None, device_name: Annotated[str | None, Form()] = None):
        super().__init__(username=username, password=password)
        self.username = username
        self.password = password
        self.device_id = device_id
        self.device_name = device_name
