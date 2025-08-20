from decimal import Decimal
from sqlalchemy import Numeric, Column, String, CHAR
from sqlmodel import Field
from .. import base


class UnitCreate(base.Unit):
    ID: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False, primary_key=True))


class UnitUpdate(base.Unit):
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    Symbol: str | None = Field(None, sa_column=Column(String(10, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    BaseID: str | None = Field(None, sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    Multiplier: Decimal | None = Field(None, sa_column=Column(Numeric(20, 10), nullable=True))
