from sqlmodel import Field
from ...schemas import base


class MethodParam(base.MethodParam):
    MethodID: int
    DataType: str | None = Field(None)
    Name: str | None = Field(None)
    Value: str | None = Field(None)


class MethodParamCreate(base.MethodParam):
    pass
