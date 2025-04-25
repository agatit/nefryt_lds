from datetime import datetime
from sqlalchemy import BINARY, BigInteger, Boolean, CHAR, Column, Float, ForeignKeyConstraint, Identity, \
    Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlmodel import SQLModel, Field
from api.schemas import EventDefBase, LdsNodeBase, LinkBase

Base = declarative_base(metadata=SQLModel.metadata)


class EventDef(EventDefBase, table=True):
    __tablename__ = 'EventDef'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True))


# TODO: test relations between method tables & how they react to cascade deleting
class MethodDef(SQLModel, table=True):
    __tablename__ = 'MethodDef'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))


class MethodParamDef(SQLModel, table=True):
    __tablename__ = 'MethodParamDef'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: str = Field(sa_column=Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False, primary_key=True))
    MethodDefID: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    DataType: str | None = Field(None, sa_column=Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=True))


class Node(LdsNodeBase, table=True):
    __tablename__ = 'Node'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1000, increment=1), primary_key=True))


class Pipeline(Base):
    __tablename__ = 'Pipeline'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='Pipeline_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=2, increment=1))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    BeginPos = Column(Numeric(10, 2))


class PipelineParamDef(Base):
    __tablename__ = 'PipelineParamDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PipelineParamDef_pk'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    DataType = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'))


class TrendData(Base):
    __tablename__ = 'TrendData'
    __table_args__ = (
        PrimaryKeyConstraint('Time', 'TrendID', name='TrendData_pk'),
        {'schema': 'lds'}
    )

    TrendID = Column(Integer, nullable=False)
    Time = Column(BigInteger, nullable=False)
    Data = Column(BINARY(200), nullable=False)


class TrendDef(Base):
    __tablename__ = 'TrendDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='TrendDef_pk'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))


class TrendGroup(Base):
    __tablename__ = 'TrendGroup'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='TrendGroup_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1, increment=1))
    Name = Column(String(100, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    AnalisisOnly = Column(Boolean, nullable=False, server_default=text('((0))'))


class Unit(Base):
    __tablename__ = 'Unit'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PK__Unit__3214EC272A787237'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    Symbol = Column(String(10, 'SQL_Polish_CP1250_CS_AS'))
    BaseID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Multiplier = Column(Numeric(20, 10))


class Link(LinkBase, table=True):
    __tablename__ = 'Link'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1, increment=1), primary_key=True))


class Method(SQLModel, table=True):
    __tablename__ = 'Method'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1000, increment=1), primary_key=True))
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


class PipelineNode(Base):
    __tablename__ = 'PipelineNode'
    __table_args__ = (
        ForeignKeyConstraint(['NodeID'], ['lds.Node.ID'], ondelete='CASCADE', onupdate='CASCADE',
                             name='PipelineNodeNode_fk'),
        ForeignKeyConstraint(['PipelineID'], ['lds.Pipeline.ID'], ondelete='CASCADE', onupdate='CASCADE',
                             name='PipelineNodePipeline_fk'),
        PrimaryKeyConstraint('PipelineID', 'NodeID', name='PipelineNode_pk'),
        {'schema': 'lds'}
    )

    PipelineID = Column(Integer, nullable=False)
    NodeID = Column(Integer, nullable=False)
    First = Column(Boolean, nullable=False, server_default=text('((0))'))

    Node_ = relationship(Node)
    Pipeline_ = relationship('Pipeline')


class PipelineParam(Base):
    __tablename__ = 'PipelineParam'
    __table_args__ = (
        ForeignKeyConstraint(['PipelineID'], ['lds.Pipeline.ID'], name='PipelineParamPipeline_fk'),
        ForeignKeyConstraint(['PipelineParamDefID'], ['lds.PipelineParamDef.ID'], ondelete='CASCADE',
                             onupdate='CASCADE', name='PipelineParamPipelineParamDef_fk'),
        PrimaryKeyConstraint('PipelineParamDefID', 'PipelineID', name='PipelineParam_pk'),
        {'schema': 'lds'}
    )

    PipelineParamDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    PipelineID = Column(Integer, nullable=False)
    Value = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Pipeline_ = relationship('Pipeline')
    PipelineParamDef_ = relationship('PipelineParamDef')


class Trend(Base):
    __tablename__ = 'Trend'
    __table_args__ = (
        ForeignKeyConstraint(['NodeID'], ['lds.Node.ID'], ondelete='SET NULL', name='Trend_fk'),
        ForeignKeyConstraint(['UnitID'], ['lds.Unit.ID'], name='Trend_Unit_fk'),
        ForeignKeyConstraint(['TrendDefID'], ['lds.TrendDef.ID'], ondelete='CASCADE', name='Trend_TrendDef_fk'),
        PrimaryKeyConstraint('ID', name='Trend_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1000, increment=1))
    TrendDefID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    RawMin = Column(Integer, nullable=False)
    RawMax = Column(Integer, nullable=False)
    ScaledMin = Column(Float(53), nullable=False)
    ScaledMax = Column(Float(53), nullable=False)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    TrendGroupID = Column(Integer)
    TimeExponent = Column(Integer)
    Format = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    UnitID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Color = Column(SmallInteger)
    Symbol = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    NodeID = Column(Integer)

    Node_ = relationship(Node)
    Unit_ = relationship('Unit')
    TrendDef_ = relationship('TrendDef')


class TrendParamDef(Base):
    __tablename__ = 'TrendParamDef'
    __table_args__ = (
        ForeignKeyConstraint(['TrendDefID'], ['lds.TrendDef.ID'], name='TrendParamDef_TrendDef_fk'),
        PrimaryKeyConstraint('ID', 'TrendDefID', name='TrendParamDef_pk'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    TrendDefID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False, index=True)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    DataType = Column(String(6, 'SQL_Polish_CP1250_CS_AS'))

    TrendDef_ = relationship('TrendDef')


class Event(SQLModel, table=True):
    __tablename__ = 'Event'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int | None = Field(default=None, primary_key=True, sa_column_kwargs={"autoincrement": True})
    EventDefID: str = (
        Field(sa_column=Column(
            CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
            ForeignKey("lds.EventDef.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False)
        ))
    MethodID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("lds.Method.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False
        ))
    BeginDate: datetime = Field(nullable=False)
    AckDate: datetime | None = Field(None)
    EndDate: datetime | None = Field(None)
    Details: str | None = Field(None, sa_column=Column(String(100, 'SQL_Polish_CP1250_CS_AS')))
    Position: int | None = Field(None)


class MethodParam(SQLModel, table=True):
    __tablename__ = 'MethodParam'
    __table_args__ = (
        {'schema': 'lds'}
    )

    MethodParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False, primary_key=True))
    MethodID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("lds.Method.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False
        ))
    Value: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))


class TrendParam(Base):
    __tablename__ = 'TrendParam'
    __table_args__ = (
        ForeignKeyConstraint(['TrendID'], ['lds.Trend.ID'], ondelete='CASCADE', onupdate='CASCADE',
                             name='TrendParam_Trend_fk'),
        PrimaryKeyConstraint('TrendParamDefID', 'TrendID', name='TrendParam_pk'),
        {'schema': 'lds'}
    )

    TrendParamDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    TrendID = Column(Integer, nullable=False)
    Value = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Trend_ = relationship('Trend')
