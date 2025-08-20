from sqlalchemy import Column, String
from sqlmodel import Field
from ...schemas import base


class TemplateCreate(base.Template):
    pass


class TemplateUpdate(base.Template):
    Name: str | None = Field(None, sa_column=Column(String(50, 'SQL_Polish_CP1250_CS_AS')))
    Axes: list[base.Axis] | None = Field(None)
