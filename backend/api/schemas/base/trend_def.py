from sqlalchemy import Column, CHAR, String
from sqlmodel import SQLModel, Field


class TrendDef(SQLModel):
    ID: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True))
    Name: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
