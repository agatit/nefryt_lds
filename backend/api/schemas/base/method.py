from sqlalchemy import Column, Integer, ForeignKey, CHAR, String
from sqlmodel import SQLModel, Field


class Method(SQLModel):
    MethodDefID: str = Field(
        sa_column=Column(
            CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
            ForeignKey("lds.MethodDef.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False
        ))
    PipelineID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("lds.Pipeline.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False
        ))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
