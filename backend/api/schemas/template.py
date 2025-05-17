from pydantic import BaseModel
from sqlalchemy import Column, String, JSON
from sqlmodel import SQLModel, Field
from api.schemas.axis import Axis


class TemplateBase(SQLModel):
    Name: str = Field(sa_column=Column(String(50, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Axes: list[Axis] = Field([], sa_column=Column(JSON))


class TemplateOut(BaseModel):
    ID: int = Field()
    Name: str = Field()
    Axes: list[Axis] = Field([])


class UpdateTemplate(SQLModel):
    Name: str | None = Field(None, sa_column=Column(String(50, 'SQL_Polish_CP1250_CS_AS')))
    Axes: list[Axis] | None = Field(None)
