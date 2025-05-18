from sqlalchemy import CHAR, Column, String, ForeignKey, Integer
from sqlmodel import SQLModel, Field


class TrendParamBase(SQLModel):
    TrendID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Trend.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    ))
    TrendParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
        nullable=False))
    Value: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS')))


class TrendParamOut(TrendParamBase):
    DataType: str | None = Field(None)
    Name: str | None = Field(None)
