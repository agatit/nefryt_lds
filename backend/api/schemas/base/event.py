from datetime import datetime
from sqlalchemy import Column, Integer, Identity, CHAR, ForeignKey, String
from sqlmodel import SQLModel, Field


class Event(SQLModel):
    ID: int = Field(sa_column=Column(Integer, Identity(start=1, increment=1), nullable=False, primary_key=True))
    EventDefID: str = (
        Field(sa_column=Column(
            CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
            ForeignKey('lds.EventDef.ID'),
            nullable=False)
        ))
    MethodID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey('lds.Method.ID'),
            nullable=False
        ))
    BeginDate: datetime = Field(nullable=False)
    AckDate: datetime | None = Field(None)
    EndDate: datetime | None = Field(None)
    Details: str | None = Field(None, sa_column=Column(String(100, 'SQL_Polish_CP1250_CS_AS')))
    Position: int | None = Field(None)
