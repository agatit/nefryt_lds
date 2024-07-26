from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import declarative_base
from . import lds

Base = declarative_base()


class Node(Base):
    __tablename__ = 'Node'
    __table_args__ = {'schema': 'editor'}

    ID = Column(ForeignKey(lds.Node.ID, ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    PosX = Column(Integer)
    PosY = Column(Integer)


class Pipeline(Base):
    __tablename__ = 'Pipeline'
    __table_args__ = {'schema': 'editor'}

    ID = Column(ForeignKey(lds.Pipeline.ID, ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    AreaWidth = Column(Integer, nullable=False)
    AreaWidthDivision = Column(Integer, nullable=False)
    AreaHeight = Column(Integer, nullable=False)
    AreaHeightDivision = Column(Integer, nullable=False)
