from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import SQLModel, Field
from api.schemas import base


class Node(base.EditorNode, table=True):
    __tablename__ = 'Node'
    __table_args__ = (
        {'schema': 'editor'}
    )

    ID: int = Field(sa_column=Column(
        Integer,
        ForeignKey('lds.Node.ID', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    ))


class Pipeline(SQLModel, table=True):
    __tablename__ = 'Pipeline'
    __table_args__ = (
        {'schema': 'editor'}
    )

    ID: int = Field(sa_column=Column(
        Integer,
        ForeignKey('lds.Pipeline.ID', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True
    ))
    AreaWidth: int = Field(Integer, nullable=False)
    AreaWidthDivision: int = Field(Integer, nullable=False)
    AreaHeight: int = Field(Integer, nullable=False)
    AreaHeightDivision: int = Field(Integer, nullable=False)
