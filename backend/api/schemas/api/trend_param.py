from sqlmodel import Field
from ...schemas import base


class TrendParam(base.TrendParam):
    TrendID: int
    DataType: str | None = Field(None)
    Name: str | None = Field(None)
    Value: str | None = Field(None)


class TrendParamCreate(base.TrendParam):
    pass
