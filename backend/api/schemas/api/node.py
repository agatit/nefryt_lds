from sqlalchemy import Column, CHAR
from sqlmodel import Field
from ...schemas import base


class Node(base.Node):
    ID: int | None = Field(None)


class NodeCreate(base.Node):
    pass


class NodeUpdate(base.LdsNode):
    Type: str | None = Field(None, sa_column=Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS')))
    EditorParams: base.EditorNode | None = Field(None)
