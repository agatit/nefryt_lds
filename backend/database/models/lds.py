from sqlalchemy import BINARY, BigInteger, Boolean, CHAR, Column, DateTime, Float, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class EventDef(Base):
    __tablename__ = 'EventDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PK_EventDef'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Verbosity = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Silent = Column(Boolean, nullable=False, server_default=text('((0))'))
    Visible = Column(Boolean, nullable=False, server_default=text('((1))'))
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))


class MethodDef(Base):
    __tablename__ = 'MethodDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='MethodDef_pk'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))


class Node(Base):
    __tablename__ = 'Node'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='Node_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1000, increment=1))
    Type = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    TrendID = Column(Integer)
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


class Link(Base):
    __tablename__ = 'Link'
    __table_args__ = (
        ForeignKeyConstraint(['BeginNodeID'], ['lds.Node.ID'], name='LinkBegineNode_fk'),
        ForeignKeyConstraint(['EndNodeID'], ['lds.Node.ID'], name='LinkEndNode_fk'),
        PrimaryKeyConstraint('ID', name='Link_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1, increment=1))
    BeginNodeID = Column(Integer)
    EndNodeID = Column(Integer)
    Length = Column(Numeric(10, 2))

    Node_ = relationship('Node', foreign_keys=[BeginNodeID])
    Node1 = relationship('Node', foreign_keys=[EndNodeID])


class Method(Base):
    __tablename__ = 'Method'
    __table_args__ = (
        ForeignKeyConstraint(['MethodDefID'], ['lds.MethodDef.ID'], ondelete='CASCADE', onupdate='CASCADE', name='Method_MethodDef_fk'),
        ForeignKeyConstraint(['PipelineID'], ['lds.Pipeline.ID'], ondelete='CASCADE', onupdate='CASCADE', name='MethodPipeline_fk'),
        PrimaryKeyConstraint('ID', name='Method_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1000, increment=1))
    MethodDefID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    PipelineID = Column(Integer, nullable=False)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    MethodDef_ = relationship('MethodDef')
    Pipeline_ = relationship('Pipeline')


class MethodParamDef(Base):
    __tablename__ = 'MethodParamDef'
    __table_args__ = (
        ForeignKeyConstraint(['MethodDefID'], ['lds.MethodDef.ID'], ondelete='CASCADE', onupdate='CASCADE', name='MethodParamDef_MethodDef_fk'),
        PrimaryKeyConstraint('ID', name='MethodParamDef_pk'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'))
    MethodDefID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    DataType = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'))

    MethodDef_ = relationship('MethodDef')


class PipelineNode(Base):
    __tablename__ = 'PipelineNode'
    __table_args__ = (
        ForeignKeyConstraint(['NodeID'], ['lds.Node.ID'], ondelete='CASCADE', onupdate='CASCADE', name='PipelineNodeNode_fk'),
        ForeignKeyConstraint(['PipelineID'], ['lds.Pipeline.ID'], ondelete='CASCADE', onupdate='CASCADE', name='PipelineNodePipeline_fk'),
        PrimaryKeyConstraint('PipelineID', 'NodeID', name='PipelineNode_pk'),
        {'schema': 'lds'}
    )

    PipelineID = Column(Integer, nullable=False)
    NodeID = Column(Integer, nullable=False)
    First = Column(Boolean, nullable=False, server_default=text('((0))'))

    Node_ = relationship('Node')
    Pipeline_ = relationship('Pipeline')


class Trend(Base):
    __tablename__ = 'Trend'
    __table_args__ = (
        ForeignKeyConstraint(['UnitID'], ['lds.Unit.ID'], name='Trend_Unit_fk'),
        PrimaryKeyConstraint('ID', name='Trend_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1000, increment=1))
    TrendDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
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

    Unit_ = relationship('Unit')


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


class Event(Base):
    __tablename__ = 'Event'
    __table_args__ = (
        ForeignKeyConstraint(['EventDefID'], ['lds.EventDef.ID'], name='Event_EventDef_fk'),
        ForeignKeyConstraint(['MethodID'], ['lds.Method.ID'], name='Event_Method_fk'),
        PrimaryKeyConstraint('ID', name='PK_Event'),
        {'schema': 'lds'}
    )

    ID = Column(BigInteger, Identity(start=1, increment=1))
    EventDefID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    MethodID = Column(Integer, nullable=False)
    BeginDate = Column(DateTime, nullable=False)
    AckDate = Column(DateTime)
    EndDate = Column(DateTime)
    Details = Column(String(100, 'SQL_Polish_CP1250_CS_AS'))
    Position = Column(Integer)

    EventDef_ = relationship('EventDef')
    Method_ = relationship('Method')


class MethodParam(Base):
    __tablename__ = 'MethodParam'
    __table_args__ = (
        ForeignKeyConstraint(['MethodID'], ['lds.Method.ID'], name='MethodParam_fk'),
        ForeignKeyConstraint(['MethodID'], ['lds.Method.ID'], ondelete='CASCADE', onupdate='CASCADE', name='MethodParamMethod_fk'),
        ForeignKeyConstraint(['MethodParamDefID'], ['lds.MethodParamDef.ID'], name='MethodParam_fk2'),
        PrimaryKeyConstraint('MethodParamDefID', 'MethodID', name='MethodParam_pk'),
        {'schema': 'lds'}
    )

    MethodParamDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    MethodID = Column(Integer, nullable=False)
    Value = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Method_ = relationship('Method', foreign_keys=[MethodID])
    Method1 = relationship('Method', foreign_keys=[MethodID])
    MethodParamDef_ = relationship('MethodParamDef')


class TrendParam(Base):
    __tablename__ = 'TrendParam'
    __table_args__ = (
        ForeignKeyConstraint(['TrendID'], ['lds.Trend.ID'], ondelete='CASCADE', onupdate='CASCADE', name='TrendParam_Trend_fk'),
        PrimaryKeyConstraint('TrendParamDefID', 'TrendID', name='TrendParam_pk'),
        {'schema': 'lds'}
    )

    TrendParamDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    TrendID = Column(Integer, nullable=False)
    Value = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Trend_ = relationship('Trend')
