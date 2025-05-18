from pydantic import BaseModel
from sqlalchemy import Column, CHAR, String
from sqlmodel import SQLModel, Field


class EditorNodeBase(SQLModel):
    PosX: int | None = Field(None)
    PosY: int | None = Field(None)


class LdsNodeBase(SQLModel):
    Type: str = Field(sa_column=Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Name: str | None = Field(None, sa_column=Column(String(50, 'SQL_Polish_CP1250_CS_AS')))


class NodeOut(BaseModel):
    ID: int | None = Field(None)
    Type: str = Field()
    TrendID: int | None = Field(None)
    Name: str | None = Field(None)
    EditorParams: EditorNodeBase | None = Field(None)


class Node(LdsNodeBase):
    EditorParams: EditorNodeBase | None = Field(None)
    TrendID: int | None = Field(None)


class UpdateNode(SQLModel):
    Type: str | None = Field(None, sa_column=Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS')))
    Name: str | None = Field(None, sa_column=Column(String(50, 'SQL_Polish_CP1250_CS_AS')))
    EditorParams: EditorNodeBase | None = Field(None)
