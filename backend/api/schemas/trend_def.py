from sqlalchemy import Column, CHAR, String
from sqlmodel import SQLModel, Field


class TrendDefBase(SQLModel):
    ID: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
