from sqlalchemy import BINARY, BigInteger, Boolean, CHAR, Column, DateTime, ForeignKey, Identity, Integer, Numeric, SmallInteger, String, text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class EventDef(Base):
    __tablename__ = 'EventDef'
    __table_args__ = {'schema': 'lds'}

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True)
    Verbosity = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Silent = Column(Boolean, nullable=False, server_default=text('((0))'))
    Visible = Column(Boolean, nullable=False, server_default=text('((1))'))
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))


class MethodDef(Base):
    __tablename__ = 'MethodDef'
    __table_args__ = {'schema': 'lds'}

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))


class Node(Base):
    __tablename__ = 'Node'
    __table_args__ = {'schema': 'lds'}

    ID = Column(Integer, Identity(start=1000, increment=1), primary_key=True)
    Type = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    TrendID = Column(Integer)
    Name = Column(String(50, 'SQL_Polish_CP1250_CS_AS'))


class Pipeline(Base):
    __tablename__ = 'Pipeline'
    __table_args__ = {'schema': 'lds'}

    ID = Column(Integer, Identity(start=2, increment=1), primary_key=True)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    BeginPos = Column(Numeric(10, 2))


class TrendData(Base):
    __tablename__ = 'TrendData'
    __table_args__ = {'schema': 'lds'}

    TrendID = Column(Integer, primary_key=True, nullable=False)
    Time = Column(BigInteger, primary_key=True, nullable=False)
    Data = Column(BINARY(200), nullable=False)


class TrendDef(Base):
    __tablename__ = 'TrendDef'
    __table_args__ = {'schema': 'lds'}

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))


class TrendGroup(Base):
    __tablename__ = 'TrendGroup'
    __table_args__ = {'schema': 'lds'}

    ID = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    Name = Column(String(100, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    AnalisisOnly = Column(Boolean, nullable=False, server_default=text('((0))'))


class Unit(Base):
    __tablename__ = 'Unit'
    __table_args__ = {'schema': 'lds'}

    ID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    Symbol = Column(String(10, 'SQL_Polish_CP1250_CS_AS'))
    BaseID = Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'))
    Multiplier = Column(Numeric(20, 10))


class Link(Base):
    __tablename__ = 'Link'
    __table_args__ = {'schema': 'lds'}

    ID = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    BeginNodeID = Column(ForeignKey('lds.Node.ID'))
    EndNodeID = Column(ForeignKey('lds.Node.ID'))
    Length = Column(Numeric(10, 2))

    Node = relationship('Node', foreign_keys=[BeginNodeID])
    Node_ = relationship('Node', foreign_keys=[EndNodeID])


class Method(Base):
    __tablename__ = 'Method'
    __table_args__ = {'schema': 'lds'}

    ID = Column(Integer, Identity(start=1000, increment=1), primary_key=True)
    MethodDefID = Column(ForeignKey('lds.MethodDef.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    PipelineID = Column(ForeignKey('lds.Pipeline.ID', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    MethodDef = relationship('MethodDef')
    Pipeline = relationship('Pipeline')


class MethodParamDef(Base):
    __tablename__ = 'MethodParamDef'
    __table_args__ = {'schema': 'lds'}

    ID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), primary_key=True)
    MethodDefID = Column(ForeignKey('lds.MethodDef.ID', ondelete='CASCADE', onupdate='CASCADE'))
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    DataType = Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'))

    MethodDef = relationship('MethodDef')


class PipelineNode(Base):
    __tablename__ = 'PipelineNode'
    __table_args__ = {'schema': 'lds'}

    ID = Column(ForeignKey('lds.Pipeline.ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, unique=True)
    NodeID = Column(ForeignKey('lds.Node.ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    First = Column(Boolean, nullable=False, server_default=text('((0))'))

    Pipeline = relationship('Pipeline')
    Node = relationship('Node')


class Trend(Base):
    __tablename__ = 'Trend'
    __table_args__ = {'schema': 'lds'}

    ID = Column(Integer, Identity(start=1000, increment=1), primary_key=True)
    TrendDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    TrendGroupID = Column(Integer)
    TimeExponent = Column(Integer)
    Format = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    UnitID = Column(ForeignKey('lds.Unit.ID'))
    Color = Column(SmallInteger)
    Symbol = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Unit = relationship('Unit')


class TrendParamDef(Base):
    __tablename__ = 'TrendParamDef'
    __table_args__ = {'schema': 'lds'}

    ID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), primary_key=True, nullable=False)
    TrendDefID = Column(ForeignKey('lds.TrendDef.ID'), primary_key=True, nullable=False, index=True)
    Name = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    DataType = Column(String(6, 'SQL_Polish_CP1250_CS_AS'))

    TrendDef = relationship('TrendDef')


class Event(Base):
    __tablename__ = 'Event'
    __table_args__ = {'schema': 'lds'}

    ID = Column(BigInteger, Identity(start=1, increment=1), primary_key=True)
    EventDefID = Column(ForeignKey('lds.EventDef.ID'), nullable=False)
    MethodID = Column(ForeignKey('lds.Method.ID'), nullable=False)
    BeginDate = Column(DateTime, nullable=False)
    AckDate = Column(DateTime)
    EndDate = Column(DateTime)
    Details = Column(String(100, 'SQL_Polish_CP1250_CS_AS'))
    Position = Column(Integer)

    EventDef = relationship('EventDef')
    Method = relationship('Method')


class MethodParam(Base):
    __tablename__ = 'MethodParam'
    __table_args__ = {'schema': 'lds'}

    MethodParamDefID = Column(ForeignKey('lds.MethodParamDef.ID'), primary_key=True, nullable=False)
    MethodID = Column(ForeignKey('lds.Method.ID', ondelete='CASCADE', onupdate='CASCADE'), ForeignKey('lds.Method.ID'), primary_key=True, nullable=False)
    Value = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Method = relationship('Method', foreign_keys=[MethodID])
    Method_ = relationship('Method', foreign_keys=[MethodID])
    MethodParamDef = relationship('MethodParamDef')


class TrendParam(Base):
    __tablename__ = 'TrendParam'
    __table_args__ = {'schema': 'lds'}

    TrendParamDefID = Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), primary_key=True, nullable=False)
    TrendID = Column(ForeignKey('lds.Trend.ID', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
    Value = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    Trend = relationship('Trend')
