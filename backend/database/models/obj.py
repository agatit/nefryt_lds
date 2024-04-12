from sqlalchemy import BigInteger, Boolean, CHAR, Column, DateTime, Float, Integer, MetaData, Numeric, String, Table
from sqlalchemy.dialects.mssql import IMAGE

metadata = MetaData()


t_Area = Table(
    'Area', metadata,
    Column('AreaID', Integer, nullable=False),
    Column('Name', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Description', String(120, 'SQL_Polish_CP1250_CS_AS')),
    schema='obj'
)


t_CommunicationCheckMode = Table(
    'CommunicationCheckMode', metadata,
    Column('CommunicationCheckModeTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('CommunicationCheckModeID', Integer, nullable=False),
    Column('Description', String(120, 'SQL_Polish_CP1250_CS_AS')),
    schema='obj'
)


t_Device = Table(
    'Device', metadata,
    Column('DeviceID', Integer, nullable=False),
    Column('DeviceDefID', Integer, nullable=False),
    Column('DriverODXID', Integer),
    Column('AdressODX', String(30, 'SQL_Polish_CP1250_CS_AS')),
    Column('EventCapableDeviceID', Integer),
    Column('ParentDeviceID', Integer),
    Column('HiddenInCommunicationDiag', Boolean, nullable=False),
    Column('Enabled', Boolean, nullable=False),
    Column('AreaID', Integer),
    Column('Symbol', String(80, 'SQL_Polish_CP1250_CS_AS')),
    Column('DeviceECNo', Integer),
    Column('EventCapable', Boolean, nullable=False),
    Column('RightAppID', Integer),
    Column('Caption', String(60, 'SQL_Polish_CP1250_CS_AS')),
    Column('MaxTimeDiff', Integer),
    schema='obj'
)


t_DeviceDef = Table(
    'DeviceDef', metadata,
    Column('DeviceDefID', Integer, nullable=False),
    Column('Caption', String(60, 'SQL_Polish_CP1250_CS_AS')),
    Column('CommunicationCheckVariableDefID', Integer),
    Column('CommunicationCheckModeTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS')),
    Column('Enabled', Boolean, nullable=False),
    schema='obj'
)


t_DriverODX = Table(
    'DriverODX', metadata,
    Column('DriverODXID', Integer, nullable=False),
    Column('Name', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('DriverClassName', String(120, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('AdressODX', String(30, 'SQL_Polish_CP1250_CS_AS')),
    Column('ConnectionString', String(200, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Enabled', Boolean, nullable=False),
    schema='obj'
)


t_DriverODXDef = Table(
    'DriverODXDef', metadata,
    Column('TID', String(120, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Name', String(100, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    schema='obj'
)


t_Event = Table(
    'Event', metadata,
    Column('EventID', BigInteger, nullable=False),
    Column('EventDefID', Integer, nullable=False),
    Column('DeviceID', Integer, nullable=False),
    Column('BeginDate', DateTime, nullable=False),
    Column('AckDate', DateTime),
    Column('EndDate', DateTime),
    Column('UserAppID', Integer),
    Column('AppName', String(128, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('DBUser', String(128, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('HostName', String(128, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('ChangeDate', DateTime),
    Column('SentSMS', Boolean, nullable=False),
    Column('SentEmail', Boolean, nullable=False),
    schema='obj'
)


t_EventDef = Table(
    'EventDef', metadata,
    Column('EventDefID', Integer, nullable=False),
    Column('EventKindDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('EventDefNo', Integer, nullable=False),
    Column('DeviceDefID', Integer, nullable=False),
    Column('VariableDefEventID', Integer),
    Column('TrendDefID', Integer),
    Column('EventRequireACKDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Caption', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Silent', Boolean, nullable=False),
    Column('IsTemporary', Boolean, nullable=False),
    Column('IncludeInAggregatedAlarm', Boolean, nullable=False),
    Column('Visible', Boolean, nullable=False),
    Column('Enabled', Boolean, nullable=False),
    schema='obj'
)


t_EventKindDef = Table(
    'EventKindDef', metadata,
    Column('EventKindDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('EventKindDefID', Integer, nullable=False),
    Column('Caption', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    schema='obj'
)


t_EventRequireACKDef = Table(
    'EventRequireACKDef', metadata,
    Column('EventRequireACKDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('EventRequireACKDefID', Integer, nullable=False),
    Column('Caption', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Enabled', Boolean, nullable=False),
    schema='obj'
)


t_EventStateDef = Table(
    'EventStateDef', metadata,
    Column('EventStateDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('EventStateDefID', Integer, nullable=False),
    Column('Name', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Description', String(120, 'SQL_Polish_CP1250_CS_AS')),
    Column('Enabled', Boolean, nullable=False),
    schema='obj'
)


t_ObjectState = Table(
    'ObjectState', metadata,
    Column('ObjectStateID', Integer, nullable=False),
    Column('Name', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Data', IMAGE),
    schema='obj'
)


t_PLCParameter = Table(
    'PLCParameter', metadata,
    Column('PLCParameterID', Integer, nullable=False),
    Column('PLCParameterDefID', Integer, nullable=False),
    Column('DeviceID', Integer, nullable=False),
    Column('Timestamp', DateTime, nullable=False),
    Column('Value', String(100, 'SQL_Polish_CP1250_CS_AS')),
    schema='obj'
)


t_PLCParameterDef = Table(
    'PLCParameterDef', metadata,
    Column('PLCParameterDefID', Integer, nullable=False),
    Column('DeviceDefID', Integer, nullable=False),
    Column('Caption', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('UnitName', String(60, 'SQL_Polish_CP1250_CS_AS')),
    Column('SynchronizeMode', Boolean, nullable=False),
    Column('AutoSend', Boolean, nullable=False),
    Column('VariableDefValueID', Integer, nullable=False),
    Column('VariableDefTimeStampID', Integer),
    Column('Enabled', Boolean, nullable=False),
    schema='obj'
)


t_Trend = Table(
    'Trend', metadata,
    Column('TrendID', BigInteger, nullable=False),
    Column('TrendDefID', Integer, nullable=False),
    Column('DeviceID', Integer, nullable=False),
    Column('Value', Float(53), nullable=False),
    Column('DateTime', DateTime, nullable=False),
    schema='obj'
)


t_TrendAgr = Table(
    'TrendAgr', metadata,
    Column('TrendAgrID', BigInteger, nullable=False),
    Column('TrendDefID', Integer, nullable=False),
    Column('DeviceID', Integer, nullable=False),
    Column('Date', DateTime, nullable=False),
    Column('FirstDT', DateTime),
    Column('FirstVal', Float(53)),
    Column('MinVal', Float(53), nullable=False),
    Column('MaxVal', Float(53)),
    Column('LastDT', DateTime),
    Column('LastVal', Float(53)),
    Column('Part', Integer),
    schema='obj'
)


t_TrendDef = Table(
    'TrendDef', metadata,
    Column('TrendDefID', Integer, nullable=False),
    Column('DeviceDefID', Integer),
    Column('VariableDefID', Integer, nullable=False),
    Column('Caption', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Interval', Integer),
    Column('Threshold', Float(24), nullable=False),
    Column('Format', String(20, 'SQL_Polish_CP1250_CS_AS')),
    Column('MaxValueWidth', Integer, nullable=False),
    Column('Color', String(8, 'SQL_Polish_CP1250_CS_AS')),
    Column('Enabled', Boolean, nullable=False),
    Column('UnitName', String(60, 'SQL_Polish_CP1250_CS_AS')),
    Column('InValueMin', Float(53), nullable=False),
    Column('InMaxValue', Float(53), nullable=False),
    Column('OutValueMin', Float(53), nullable=False),
    Column('OutValueMax', Float(53), nullable=False),
    schema='obj'
)


t_VariableAccesDef = Table(
    'VariableAccesDef', metadata,
    Column('VariableAccesDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('VariableAccesDefID', Integer, nullable=False),
    Column('Name', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Description', String(120, 'SQL_Polish_CP1250_CS_AS')),
    schema='obj'
)


t_VariableDef = Table(
    'VariableDef', metadata,
    Column('VariableDefID', Integer, nullable=False),
    Column('DeviceDefID', Integer, nullable=False),
    Column('Alias', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('AdressODX', String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('VariableAccesDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('VariableTypeDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('RefreshTime', Integer, nullable=False),
    Column('Threshold', Integer, nullable=False),
    Column('DestroyWithLastClient', Boolean, nullable=False),
    Column('VariableSize', Integer),
    Column('Enabled', Boolean, nullable=False),
    Column('VariableScaleDefID', Integer),
    schema='obj'
)


t_VariableScaleDef = Table(
    'VariableScaleDef', metadata,
    Column('VariableScaleDefID', Integer, nullable=False),
    Column('Name', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Description', String(120, 'SQL_Polish_CP1250_CS_AS')),
    Column('ValueMin', Numeric(18, 8), nullable=False),
    Column('ValueMax', Numeric(18, 8), nullable=False),
    Column('RangeMin', Numeric(18, 8), nullable=False),
    Column('RangeMax', Numeric(18, 8), nullable=False),
    schema='obj'
)


t_VariableTypeDef = Table(
    'VariableTypeDef', metadata,
    Column('VariableTypeDefTID', CHAR(8, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('VariableTypeDefID', Integer, nullable=False),
    Column('Name', String(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False),
    Column('Description', String(120, 'SQL_Polish_CP1250_CS_AS')),
    Column('DelphiCode', Integer),
    schema='obj'
)
