from sqlalchemy import BigInteger, Boolean, CHAR, Column, DateTime, Float, ForeignKeyConstraint, Identity, Index, Integer, Numeric, PrimaryKeyConstraint, String, text
from sqlalchemy.dialects.mssql import IMAGE
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Area(Base):
    __tablename__ = 'Area'
    __table_args__ = (
        PrimaryKeyConstraint('AreaID', name='PK_Area'),
        {'schema': 'obj'}
    )

    AreaID = Column(Integer)
    Name = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    Description = Column(String(120, 'SQL_Polish_CP1250_CS_AS'))


class CommunicationCheckMode(Base):
    __tablename__ = 'CommunicationCheckMode'
    __table_args__ = (
        PrimaryKeyConstraint('CommunicationCheckModeID', name='PK_CommunicationCheckMode'),
        {'schema': 'obj'}
    )

    CommunicationCheckModeTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    CommunicationCheckModeID = Column(Integer, Identity(start=1, increment=1))
    Description = Column(String(120, 'SQL_Polish_CP1250_CS_AS'))


class DeviceDef(Base):
    __tablename__ = 'DeviceDef'
    __table_args__ = (
        ForeignKeyConstraint(['CommunicationCheckModeTID'], ['obj.CommunicationCheckMode.CommunicationCheckModeTID'], name='FK_DevicePartDef_CommunicationCheckModeTID'),
        ForeignKeyConstraint(['CommunicationCheckVariableDefID'], ['obj.VariableDef.VariableDefID'], name='FK_DevicePartDef_CommunicationCheckVariableDefID'),
        PrimaryKeyConstraint('DeviceDefID', name='PK_DevicePartDef'),
        {'schema': 'obj'}
    )

    DeviceDefID = Column(Integer)
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'))
    CommunicationCheckVariableDefID = Column(Integer, index=True)
    CommunicationCheckModeTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), index=True)

    CommunicationCheckMode_ = relationship('CommunicationCheckMode')
    VariableDef = relationship('VariableDef', foreign_keys=[CommunicationCheckVariableDefID])


class DriverODXDef(Base):
    __tablename__ = 'DriverODXDef'
    __table_args__ = (
        PrimaryKeyConstraint('TID', name='PK__DriverOD__C456D729D1426DB3'),
        {'schema': 'obj'}
    )

    TID = Column(String(120, 'SQL_Polish_CP1250_CS_AS'))
    Name = Column(String(100, 'SQL_Polish_CP1250_CS_AS'), nullable=False)


class EventKindDef(Base):
    __tablename__ = 'EventKindDef'
    __table_args__ = (
        PrimaryKeyConstraint('EventKindDefID', name='PK_EventKind'),
        {'schema': 'obj'}
    )

    EventKindDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    EventKindDefID = Column(Integer, Identity(start=1, increment=1))
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)


class EventRequireACKDef(Base):
    __tablename__ = 'EventRequireACKDef'
    __table_args__ = (
        PrimaryKeyConstraint('EventRequireACKDefID', name='PK_EventRequireACKDef'),
        {'schema': 'obj'}
    )

    EventRequireACKDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    EventRequireACKDefID = Column(Integer, Identity(start=1, increment=1))
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))


class EventStateDef(Base):
    __tablename__ = 'EventStateDef'
    __table_args__ = (
        PrimaryKeyConstraint('EventStateDefID', name='PK_EventStateDef'),
        {'schema': 'obj'}
    )

    EventStateDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    EventStateDefID = Column(Integer, Identity(start=1, increment=1))
    Name = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))
    Description = Column(String(120, 'SQL_Polish_CP1250_CS_AS'))


class ObjectState(Base):
    __tablename__ = 'ObjectState'
    __table_args__ = (
        PrimaryKeyConstraint('ObjectStateID', name='PK_ObjectState_ObjectStateID'),
        {'schema': 'obj'}
    )

    ObjectStateID = Column(Integer, Identity(start=1, increment=1))
    Name = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    Data = Column(IMAGE)


class VariableAccesDef(Base):
    __tablename__ = 'VariableAccesDef'
    __table_args__ = (
        PrimaryKeyConstraint('VariableAccesDefID', name='PK_VariableAccesDef'),
        {'schema': 'obj'}
    )

    VariableAccesDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    VariableAccesDefID = Column(Integer, Identity(start=1, increment=1))
    Name = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    Description = Column(String(120, 'SQL_Polish_CP1250_CS_AS'))


class VariableDef(Base):
    __tablename__ = 'VariableDef'
    __table_args__ = (
        ForeignKeyConstraint(['DeviceDefID'], ['obj.DeviceDef.DeviceDefID'], name='FK_VariableDef_DevicePartDefID'),
        ForeignKeyConstraint(['VariableAccesDefTID'], ['obj.VariableAccesDef.VariableAccesDefTID'], name='FK_VariableDef_VariableAccesDefTID'),
        ForeignKeyConstraint(['VariableScaleDefID'], ['obj.VariableScaleDef.VariableScaleDefID'], name='FK_VariableDef_VariableSceleDefID'),
        ForeignKeyConstraint(['VariableTypeDefTID'], ['obj.VariableTypeDef.VariableTypeDefTID'], name='FK_VariableDef_VariableTypeDefTID'),
        PrimaryKeyConstraint('VariableDefID', name='PK_VariableDef'),
        Index('UQ_VariableDef_Alias', 'Alias', 'DeviceDefID', unique=True),
        {'schema': 'obj'}
    )

    VariableDefID = Column(Integer, Identity(start=1, increment=1))
    DeviceDefID = Column(Integer, nullable=False, index=True)
    Alias = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    AdressODX = Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    VariableAccesDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, index=True, server_default=text("('RO')"))
    VariableTypeDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, index=True)
    RefreshTime = Column(Integer, nullable=False, server_default=text('((1000))'))
    Threshold = Column(Integer, nullable=False, server_default=text('((0))'))
    DestroyWithLastClient = Column(Boolean, nullable=False, server_default=text('((0))'))
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))
    VariableSize = Column(Integer)
    VariableScaleDefID = Column(Integer)

    DeviceDef_ = relationship('DeviceDef', foreign_keys=[DeviceDefID])
    VariableAccesDef_ = relationship('VariableAccesDef')
    VariableScaleDef = relationship('VariableScaleDef')
    VariableTypeDef = relationship('VariableTypeDef')


class VariableScaleDef(Base):
    __tablename__ = 'VariableScaleDef'
    __table_args__ = (
        PrimaryKeyConstraint('VariableScaleDefID', name='PK_VariableScaleDef'),
        {'schema': 'obj'}
    )

    VariableScaleDefID = Column(Integer, Identity(start=1, increment=1))
    Name = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    ValueMin = Column(Numeric(18, 8), nullable=False)
    ValueMax = Column(Numeric(18, 8), nullable=False)
    RangeMin = Column(Numeric(18, 8), nullable=False)
    RangeMax = Column(Numeric(18, 8), nullable=False)
    Description = Column(String(120, 'SQL_Polish_CP1250_CS_AS'))


class VariableTypeDef(Base):
    __tablename__ = 'VariableTypeDef'
    __table_args__ = (
        PrimaryKeyConstraint('VariableTypeDefID', name='PK_VariableTypeDef'),
        {'schema': 'obj'}
    )

    VariableTypeDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    VariableTypeDefID = Column(Integer, Identity(start=1, increment=1))
    Name = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    Description = Column(String(120, 'SQL_Polish_CP1250_CS_AS'))
    DelphiCode = Column(Integer)


class DriverODX(Base):
    __tablename__ = 'DriverODX'
    __table_args__ = (
        ForeignKeyConstraint(['DriverClassName'], ['obj.DriverODXDef.TID'], name='FK_DriverODX_Def'),
        PrimaryKeyConstraint('DriverODXID', name='PK_DriverODX'),
        {'schema': 'obj'}
    )

    DriverODXID = Column(Integer, Identity(start=1, increment=1))
    Name = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False, unique=True)
    DriverClassName = Column(String(120, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    ConnectionString = Column(String(200, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))
    AdressODX = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))

    DriverODXDef_ = relationship('DriverODXDef')


class PLCParameterDef(Base):
    __tablename__ = 'PLCParameterDef'
    __table_args__ = (
        ForeignKeyConstraint(['DeviceDefID'], ['obj.DeviceDef.DeviceDefID'], name='FK_PLCParameterDef_DeviceDefID'),
        ForeignKeyConstraint(['VariableDefTimeStampID'], ['obj.VariableDef.VariableDefID'], name='FK_PLCParameterDef_VariableDefTimeStampID'),
        ForeignKeyConstraint(['VariableDefValueID'], ['obj.VariableDef.VariableDefID'], name='FK_PLCParameterDef_VariableDefValueID'),
        PrimaryKeyConstraint('PLCParameterDefID', name='PK_PLCParameterDef'),
        Index('UQ_PLCParameterDef_DeviceDefID_Caption', 'DeviceDefID', 'Caption', unique=True),
        {'schema': 'obj'}
    )

    PLCParameterDefID = Column(Integer, Identity(start=0, increment=1))
    DeviceDefID = Column(Integer, nullable=False)
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    SynchronizeMode = Column(Boolean, nullable=False)
    AutoSend = Column(Boolean, nullable=False, server_default=text('((0))'))
    VariableDefValueID = Column(Integer, nullable=False)
    Enabled = Column(Boolean, nullable=False, server_default=text('((0))'))
    UnitName = Column(String(60, 'SQL_Polish_CP1250_CS_AS'))
    VariableDefTimeStampID = Column(Integer)

    DeviceDef_ = relationship('DeviceDef')
    VariableDef_ = relationship('VariableDef', foreign_keys=[VariableDefTimeStampID])
    VariableDef1 = relationship('VariableDef', foreign_keys=[VariableDefValueID])


class TrendDef(Base):
    __tablename__ = 'TrendDef'
    __table_args__ = (
        ForeignKeyConstraint(['VariableDefID'], ['obj.VariableDef.VariableDefID'], name='FK_TrendDef_VariableDefID'),
        PrimaryKeyConstraint('TrendDefID', name='PK_TrendDef'),
        {'schema': 'obj'}
    )

    TrendDefID = Column(Integer, Identity(start=1, increment=1))
    VariableDefID = Column(Integer, nullable=False, index=True)
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Threshold = Column(Float(24), nullable=False, server_default=text('((10))'))
    MaxValueWidth = Column(Integer, nullable=False, server_default=text('((100))'))
    Enabled = Column(Boolean, nullable=False, server_default=text('((0))'))
    InValueMin = Column(Float(53), nullable=False, server_default=text('((0))'))
    InMaxValue = Column(Float(53), nullable=False, server_default=text('((100))'))
    OutValueMin = Column(Float(53), nullable=False, server_default=text('((0))'))
    OutValueMax = Column(Float(53), nullable=False, server_default=text('((100))'))
    DeviceDefID = Column(Integer, index=True)
    Interval = Column(Integer, server_default=text('((900))'))
    Format = Column(String(20, 'SQL_Polish_CP1250_CS_AS'))
    Color = Column(String(8, 'SQL_Polish_CP1250_CS_AS'))
    UnitName = Column(String(60, 'SQL_Polish_CP1250_CS_AS'))

    VariableDef_ = relationship('VariableDef')


class Device(Base):
    __tablename__ = 'Device'
    __table_args__ = (
        ForeignKeyConstraint(['DeviceDefID'], ['obj.DeviceDef.DeviceDefID'], name='FK_DevicePart_DevicePartDefID'),
        ForeignKeyConstraint(['DriverODXID'], ['obj.DriverODX.DriverODXID'], name='FK_DevicePart_DriverODXID'),
        PrimaryKeyConstraint('DeviceID', name='Device_pk'),
        {'schema': 'obj'}
    )

    DeviceID = Column(Integer, unique=True)
    DeviceDefID = Column(Integer, nullable=False)
    HiddenInCommunicationDiag = Column(Boolean, nullable=False, server_default=text('((0))'))
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))
    EventCapable = Column(Boolean, nullable=False, server_default=text('((1))'))
    DriverODXID = Column(Integer)
    AdressODX = Column(String(30, 'SQL_Polish_CP1250_CS_AS'))
    EventCapableDeviceID = Column(Integer, index=True)
    ParentDeviceID = Column(Integer)
    AreaID = Column(Integer)
    Symbol = Column(String(80, 'SQL_Polish_CP1250_CS_AS'))
    DeviceECNo = Column(Integer)
    RightAppID = Column(Integer)
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'))
    MaxTimeDiff = Column(Integer)

    DeviceDef_ = relationship('DeviceDef')
    DriverODX_ = relationship('DriverODX')


class EventDef(Base):
    __tablename__ = 'EventDef'
    __table_args__ = (
        ForeignKeyConstraint(['EventKindDefTID'], ['obj.EventKindDef.EventKindDefTID'], name='FK_EventDef_EventKindDefTID'),
        ForeignKeyConstraint(['EventRequireACKDefTID'], ['obj.EventRequireACKDef.EventRequireACKDefTID'], name='FK_EventDef_EventRequireACKDefTID'),
        ForeignKeyConstraint(['TrendDefID'], ['obj.TrendDef.TrendDefID'], name='FK_EventDef_TrendDefID'),
        ForeignKeyConstraint(['VariableDefEventID'], ['obj.VariableDef.VariableDefID'], name='FK_EventDef_VariableDefEventID'),
        PrimaryKeyConstraint('EventDefID', name='PK_EventDef'),
        Index('UQ_EventDef_DeviceDefID_Caption_TrendDefID', 'DeviceDefID', 'Caption'),
        Index('UQ_EventDef_DeviceDefID_EventDefNo', 'DeviceDefID', 'EventDefNo', unique=True),
        {'schema': 'obj'}
    )

    EventDefID = Column(Integer)
    EventKindDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, index=True)
    EventDefNo = Column(Integer, nullable=False)
    DeviceDefID = Column(Integer, nullable=False)
    EventRequireACKDefTID = Column(CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False, index=True)
    Caption = Column(String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    Silent = Column(Boolean, nullable=False, server_default=text('((0))'))
    IsTemporary = Column(Boolean, nullable=False, server_default=text('((0))'))
    IncludeInAggregatedAlarm = Column(Boolean, nullable=False, server_default=text('((0))'))
    Visible = Column(Boolean, nullable=False, server_default=text('((1))'))
    Enabled = Column(Boolean, nullable=False, server_default=text('((1))'))
    VariableDefEventID = Column(Integer, index=True)
    TrendDefID = Column(Integer, index=True)

    EventKindDef_ = relationship('EventKindDef')
    EventRequireACKDef_ = relationship('EventRequireACKDef')
    TrendDef_ = relationship('TrendDef')
    VariableDef_ = relationship('VariableDef')


class Trend(Base):
    __tablename__ = 'Trend'
    __table_args__ = (
        ForeignKeyConstraint(['TrendDefID'], ['obj.TrendDef.TrendDefID'], name='FK_Trend_TrendDefID'),
        PrimaryKeyConstraint('DateTime', 'TrendDefID', 'DeviceID', 'TrendID', name='PK_Trend_DateTrendDefIDDeviceIDTrendID'),
        Index('Trend_idx', 'TrendDefID', 'DeviceID', 'DateTime'),
        {'schema': 'obj'}
    )

    TrendID = Column(BigInteger, Identity(start=1, increment=1), nullable=False)
    TrendDefID = Column(Integer, nullable=False)
    DeviceID = Column(Integer, nullable=False)
    Value = Column(Float(53), nullable=False)
    DateTime_ = Column('DateTime', DateTime, nullable=False)

    TrendDef_ = relationship('TrendDef')


class TrendAgr(Base):
    __tablename__ = 'TrendAgr'
    __table_args__ = (
        ForeignKeyConstraint(['TrendDefID'], ['obj.TrendDef.TrendDefID'], name='FK_TrendDayAgr_TrendDefID'),
        PrimaryKeyConstraint('Date', 'TrendDefID', 'DeviceID', 'TrendAgrID', name='PK_TrendDayAgr_DateTrendDefIDDeviceIDTrendID'),
        Index('TrendAgr_idx', 'TrendDefID', 'DeviceID', 'Date', 'Part'),
        Index('TrendDayAgr_idx', 'TrendDefID', 'DeviceID', 'Date'),
        {'schema': 'obj'}
    )

    TrendAgrID = Column(BigInteger, Identity(start=1, increment=1), nullable=False)
    TrendDefID = Column(Integer, nullable=False)
    DeviceID = Column(Integer, nullable=False)
    Date = Column(DateTime, nullable=False)
    MinVal = Column(Float(53), nullable=False)
    FirstDT = Column(DateTime)
    FirstVal = Column(Float(53))
    MaxVal = Column(Float(53))
    LastDT = Column(DateTime)
    LastVal = Column(Float(53))
    Part = Column(Integer)

    TrendDef_ = relationship('TrendDef')


class Event(Base):
    __tablename__ = 'Event'
    __table_args__ = (
        ForeignKeyConstraint(['EventDefID'], ['obj.EventDef.EventDefID'], name='FK_Event_EventDefID'),
        PrimaryKeyConstraint('BeginDate', 'EventDefID', 'DeviceID', 'EventID', name='PK_Event'),
        {'schema': 'obj'}
    )

    EventID = Column(BigInteger, Identity(start=1, increment=1), nullable=False, unique=True)
    EventDefID = Column(Integer, nullable=False)
    DeviceID = Column(Integer, nullable=False)
    BeginDate = Column(DateTime, nullable=False)
    AppName = Column(String(128, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    DBUser = Column(String(128, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    HostName = Column(String(128, 'SQL_Polish_CP1250_CS_AS'), nullable=False)
    SentSMS = Column(Boolean, nullable=False, server_default=text('((0))'))
    SentEmail = Column(Boolean, nullable=False, server_default=text('((0))'))
    AckDate = Column(DateTime)
    EndDate = Column(DateTime)
    UserAppID = Column(Integer)
    ChangeDate = Column(DateTime)

    EventDef_ = relationship('EventDef')


class PLCParameter(Base):
    __tablename__ = 'PLCParameter'
    __table_args__ = (
        ForeignKeyConstraint(['DeviceID'], ['obj.Device.DeviceID'], name='FK_PLCParameter_DeviceID'),
        ForeignKeyConstraint(['PLCParameterDefID'], ['obj.PLCParameterDef.PLCParameterDefID'], name='FK_PLCParameter_PLCParameterDefID'),
        PrimaryKeyConstraint('PLCParameterID', name='PK_PLCParameter'),
        Index('UQ_PLCParameter_PLCParameterDefID_DeviceID', 'PLCParameterDefID', 'DeviceID', unique=True),
        {'schema': 'obj'}
    )

    PLCParameterID = Column(Integer, Identity(start=0, increment=1))
    PLCParameterDefID = Column(Integer, nullable=False)
    DeviceID = Column(Integer, nullable=False)
    Timestamp = Column(DateTime, nullable=False)
    Value = Column(String(100, 'SQL_Polish_CP1250_CS_AS'))

    Device_ = relationship('Device')
    PLCParameterDef_ = relationship('PLCParameterDef')
