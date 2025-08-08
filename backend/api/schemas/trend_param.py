from sqlalchemy import CHAR, Column, String
from sqlmodel import SQLModel, Field


class TrendParamBase(SQLModel):
    TrendParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
        nullable=False))
    Value: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS')))


class TrendParamOut(TrendParamBase):
    TrendID: int
    DataType: str | None = Field(None)
    Name: str | None = Field(None)
