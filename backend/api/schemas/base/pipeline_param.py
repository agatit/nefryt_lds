from sqlalchemy import Column, String, CHAR
from sqlmodel import SQLModel, Field


class PipelineParam(SQLModel):
    PipelineParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
        nullable=False))
    Value: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
