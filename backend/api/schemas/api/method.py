from sqlalchemy import Column, Integer, ForeignKey, CHAR, String
from sqlmodel import Field
from ...schemas import base


class MethodCreate(base.Method):
    pass


class MethodUpdate(base.Method):
    MethodDefID: str | None = Field(None,
        sa_column=Column(
            CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
            ForeignKey("lds.MethodDef.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=True
        ))
    PipelineID: int | None = Field(None,
        sa_column=Column(
            Integer,
            ForeignKey("lds.Pipeline.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=True
        ))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
