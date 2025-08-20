from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field


class TrendGroup(SQLModel):
    Name: str = Field(sa_column=Column(String(100, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    AnalysisOnly: bool = Field(False, nullable=False, sa_column_kwargs={"server_default": "0"})
