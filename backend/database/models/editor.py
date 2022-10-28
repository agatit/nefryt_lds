from sqlalchemy import CHAR, Column, ForeignKeyConstraint, Identity, Integer, Numeric, PrimaryKeyConstraint, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Node(Base):
    __tablename__ = 'Node'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='Node_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1000, increment=1))
    Type = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Name = Column(String(50, 'SQL_Polish_CP1250_CS_AS'))


class Pipeline(Base):
    __tablename__ = 'Pipeline'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='Pipeline_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=2, increment=1))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    BeginPos = Column(Numeric(10, 2))


class Node_(Node):
    __tablename__ = 'Node'
    __table_args__ = (
        ForeignKeyConstraint(['ID'], ['lds.Node.ID'], ondelete='CASCADE', onupdate='CASCADE', name='Node_fk'),
        PrimaryKeyConstraint('ID', name='PK__Node__3214EC271A0EE322'),
        {'schema': 'editor'}
    )

    ID = Column(Integer)
    PosX = Column(Integer)
    PosY = Column(Integer)


class Pipeline_(Pipeline):
    __tablename__ = 'Pipeline'
    __table_args__ = (
        ForeignKeyConstraint(['ID'], ['lds.Pipeline.ID'], ondelete='CASCADE', onupdate='CASCADE', name='Pipeline_fk'),
        PrimaryKeyConstraint('ID', name='PK__Pipeline__3214EC27EF3C5111'),
        {'schema': 'editor'}
    )

    ID = Column(Integer)
    AreaWidth = Column(Integer, nullable=False)
    AreaWidthDivision = Column(Integer, nullable=False)
    AreaHeight = Column(Integer, nullable=False)
    AreaHeightDivision = Column(Integer, nullable=False)
