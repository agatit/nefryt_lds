from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field


class Pipeline(SQLModel):
    Name: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
