from pydantic import BaseModel
from sqlalchemy import Column, String, JSON
from sqlmodel import SQLModel, Field


class Axis(BaseModel):
    TrendsID: list[int] = Field([])
    Title: str = Field()
    UnitID: str = Field()
    ScaledMin: float = Field()
    ScaledMax: float = Field()


class Template(SQLModel):
    Name: str = Field(sa_column=Column(String(50, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Axes: list[Axis] = Field([], sa_column=Column(JSON))

