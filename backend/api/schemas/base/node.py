from sqlalchemy import Column, CHAR, String
from sqlmodel import SQLModel, Field


class EditorNode(SQLModel):
    PosX: int | None = Field(None)
    PosY: int | None = Field(None)


class LdsNode(SQLModel):
    Type: str = Field(sa_column=Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Name: str | None = Field(None, sa_column=Column(String(50, 'SQL_Polish_CP1250_CS_AS')))


class Node(LdsNode):
    EditorParams: EditorNode | None = Field(None)
    TrendID: int | None = Field(None)
