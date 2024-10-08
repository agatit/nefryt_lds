from sqlalchemy import BINARY, BigInteger, Boolean, CHAR, Column, DateTime, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, SmallInteger, String, text
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

    Event = relationship('Event', back_populates='EventDef_')


class MethodDef(Base):
    __tablename__ = 'MethodDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='MethodDef_pk'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Method = relationship('Method', back_populates='MethodDef_')


class MethodParamDef(Base):
    __tablename__ = 'MethodParamDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', 'MethodDefID', name='MethodParamDef_pk'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False, index=True)
    MethodDefID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    DataType = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'))


class Node(Base):
    __tablename__ = 'Node'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='Node_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1000, increment=1))
    Type = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Name = Column(String(50, 'SQL_Polish_CP1250_CS_AS'))

    Link = relationship('Link', foreign_keys='[Link.BeginNodeID]', back_populates='Node_')
    Link_ = relationship('Link', foreign_keys='[Link.EndNodeID]', back_populates='Node1')
    PipelineNode = relationship('PipelineNode', back_populates='Node_')
    Trend = relationship('Trend', back_populates='Node_')


class Pipeline(Base):
    __tablename__ = 'Pipeline'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='Pipeline_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=2, increment=1))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    BeginPos = Column(Numeric(10, 2))

    Method = relationship('Method', back_populates='Pipeline_')
    PipelineNode = relationship('PipelineNode', back_populates='Pipeline_')
    PipelineParam = relationship('PipelineParam', back_populates='Pipeline_')


class PipelineParamDef(Base):
    __tablename__ = 'PipelineParamDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', name='PipelineParamDef_pk'),
        {'schema': 'lds'}
    )

    ID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    DataType = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'))

    PipelineParam = relationship('PipelineParam', back_populates='PipelineParamDef_')


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

    TrendParamDef = relationship('TrendParamDef', back_populates='TrendDef_')


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

    Trend = relationship('Trend', back_populates='Unit_')


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

    Node_ = relationship('Node', foreign_keys=[BeginNodeID], back_populates='Link')
    Node1 = relationship('Node', foreign_keys=[EndNodeID], back_populates='Link_')


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

    MethodDef_ = relationship('MethodDef', back_populates='Method')
    Pipeline_ = relationship('Pipeline', back_populates='Method')
    Event = relationship('Event', back_populates='Method_')
    MethodParam = relationship('MethodParam', back_populates='Method_')


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

    Node_ = relationship('Node', back_populates='PipelineNode')
    Pipeline_ = relationship('Pipeline', back_populates='PipelineNode')


class PipelineParam(Base):
    __tablename__ = 'PipelineParam'
    __table_args__ = (
        ForeignKeyConstraint(['PipelineID'], ['lds.Pipeline.ID'], name='PipelineParamPipeline_fk'),
        ForeignKeyConstraint(['PipelineParamDefID'], ['lds.PipelineParamDef.ID'], ondelete='CASCADE', onupdate='CASCADE', name='PipelineParamPipelineParamDef_fk'),
        PrimaryKeyConstraint('PipelineParamDefID', 'PipelineID', name='PipelineParam_pk'),
        {'schema': 'lds'}
    )

    PipelineParamDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    PipelineID = Column(Integer, nullable=False)
    Value = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Pipeline_ = relationship('Pipeline', back_populates='PipelineParam')
    PipelineParamDef_ = relationship('PipelineParamDef', back_populates='PipelineParam')


class Trend(Base):
    __tablename__ = 'Trend'
    __table_args__ = (
        ForeignKeyConstraint(['NodeID'], ['lds.Node.ID'], ondelete='SET NULL', name='Trend_fk'),
        ForeignKeyConstraint(['UnitID'], ['lds.Unit.ID'], name='Trend_Unit_fk'),
        PrimaryKeyConstraint('ID', name='Trend_pk'),
        {'schema': 'lds'}
    )

    ID = Column(Integer, Identity(start=1000, increment=1))
    TrendDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    TrendGroupID = Column(Integer)
    TimeExponent = Column(Integer)
    Format = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    UnitID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Color = Column(SmallInteger)
    Symbol = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    NodeID = Column(Integer)

    Node_ = relationship('Node', back_populates='Trend')
    Unit_ = relationship('Unit', back_populates='Trend')
    TrendParam = relationship('TrendParam', back_populates='Trend_')


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

    TrendDef_ = relationship('TrendDef', back_populates='TrendParamDef')


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

    EventDef_ = relationship('EventDef', back_populates='Event')
    Method_ = relationship('Method', back_populates='Event')


class MethodParam(Base):
    __tablename__ = 'MethodParam'
    __table_args__ = (
        ForeignKeyConstraint(['MethodID'], ['lds.Method.ID'], name='MethodParamMethod_fk'),
        PrimaryKeyConstraint('MethodParamDefID', 'MethodID', name='MethodParam_pk'),
        {'schema': 'lds'}
    )

    MethodParamDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    MethodID = Column(Integer, nullable=False)
    Value = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Method_ = relationship('Method', back_populates='MethodParam')


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

    Trend_ = relationship('Trend', back_populates='TrendParam')
