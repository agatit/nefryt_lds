from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import declarative_base
from sqlmodel import SQLModel, Field
from api.schemas import EditorNodeBase
from . import lds

Base = declarative_base(metadata=SQLModel.metadata)


class Node(EditorNodeBase, table=True):
    __tablename__ = 'Node'
    __table_args__ = (
        {'schema': 'editor'}
    )

    ID: int = Field(sa_column=Column(ForeignKey('lds.Node.ID', ondelete='CASCADE', onupdate='CASCADE'),
                                     primary_key=True))


class Pipeline(Base):
    __tablename__ = 'Pipeline'
    __table_args__ = {'schema': 'editor'}

    ID = Column(ForeignKey(lds.Pipeline.ID, ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    AreaWidth = Column(Integer, nullable=False)
    AreaWidthDivision = Column(Integer, nullable=False)
    AreaHeight = Column(Integer, nullable=False)
    AreaHeightDivision = Column(Integer, nullable=False)
