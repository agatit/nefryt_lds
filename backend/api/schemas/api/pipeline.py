from sqlalchemy import Column, String
from sqlmodel import Field
from ...schemas import base


class PipelineCreate(base.Pipeline):
    pass


class PipelineUpdate(base.Pipeline):
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
