from sqlalchemy import Column, String
from sqlmodel import Field
from ...schemas import base


class TrendGroupCreate(base.TrendGroup):
    pass


class TrendGroupUpdate(base.TrendGroup):
    Name: str | None = Field(None, sa_column=Column(String(100, 'SQL_Polish_CP1250_CS_AS')))
    AnalysisOnly: bool | None = Field(None)
