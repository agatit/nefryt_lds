from decimal import Decimal
from sqlalchemy import Numeric, Column, String, CHAR
from sqlmodel import SQLModel, Field


class Unit(SQLModel):
    Name: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Symbol: str = Field(sa_column=Column(String(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    BaseID: str | None = Field(None, sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    Multiplier: Decimal | None = Field(None, sa_column=Column(Numeric(20, 10), nullable=True))
