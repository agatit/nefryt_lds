from datetime import datetime
from sqlalchemy import BINARY, BigInteger, CHAR, Column, Identity, \
    Integer, PrimaryKeyConstraint, String, ForeignKey, VARCHAR, ForeignKeyConstraint, Index, Float
from sqlmodel import SQLModel, Field
from api.schemas import base


class EventDef(base.EventDef, table=True):
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


class Node(base.LdsNode, table=True):
    __tablename__ = 'Node'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1000, increment=1), primary_key=True))


class Pipeline(base.Pipeline, table=True):
    __tablename__ = 'Pipeline'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=2, increment=1), primary_key=True))


class PipelineParamDef(SQLModel, table=True):
    __tablename__ = 'PipelineParamDef'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: str = Field(sa_column=Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False, primary_key=True))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    DataType: str | None = Field(None, sa_column=Column(CHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=True))


class TrendData(SQLModel, table=True):
    __tablename__ = 'TrendData'
    __table_args__ = (
        PrimaryKeyConstraint('Time', 'TrendID', name='TrendData_pk'),
        Index("idx_time_trendid", "TrendID", "Time", unique=True),
        {'schema': 'lds'}
    )

    TrendID: int = Field(sa_column=Column(Integer, nullable=False))
    Time: int = Field(sa_column=Column(BigInteger, nullable=False))
    Data: bytes = Field(sa_column=Column(BINARY(200), nullable=False))


class PastTrendData(SQLModel, table=True):
    __tablename__ = 'PastTrendData'
    __table_args__ = (
        PrimaryKeyConstraint('Time', 'TrendID', name='PastTrendData_pk'),
        Index("past_idx_time_trendid", "TrendID", "Time", unique=True),
        {'schema': 'lds'}
    )

    TrendID: int = Field(sa_column=Column(Integer, nullable=False))
    Time: int = Field(sa_column=Column(BigInteger, nullable=False))
    Data: bytes = Field(sa_column=Column(BINARY(200), nullable=False))


class TrendDef(base.TrendDef, table=True):
    __tablename__ = 'TrendDef'
    __table_args__ = (
        {'schema': 'lds'}
    )


class TrendGroup(base.TrendGroup, table=True):
    __tablename__ = 'TrendGroup'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1, increment=1), primary_key=True, nullable=False))


class Unit(base.Unit, table=True):
    __tablename__ = 'Unit'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False, primary_key=True))


class Link(base.Link, table=True):
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


class PipelineNode(SQLModel, table=True):
    __tablename__ = 'PipelineNode'
    __table_args__ = (
        PrimaryKeyConstraint('PipelineID', 'NodeID', name='PipelineNode_pk'),
        {'schema': 'lds'}
    )

    PipelineID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("lds.Pipeline.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False
        ))
    NodeID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("lds.Node.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False
        ))
    First: bool = Field(False, nullable=False, sa_column_kwargs={"server_default": "0"})


class PipelineParam(base.PipelineParam, table=True):
    __tablename__ = 'PipelineParam'
    __table_args__ = (
        PrimaryKeyConstraint('PipelineParamDefID', 'PipelineID', name='PipelineParam_pk'),
        {'schema': 'lds'}
    )

    PipelineID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("lds.Pipeline.ID"),
            nullable=False
        )
    )


class Trend(base.Trend, table=True):
    __tablename__ = 'Trend'
    __table_args__ = (
        ForeignKeyConstraint(
            ['TrendDefID'], ['lds.TrendDef.ID'],
            name='Trend_TrendDef_fk',
            ondelete='CASCADE'
        ),
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1000, increment=1), nullable=False, primary_key=True))
    TimeDelta: int = Field(0, nullable=False)
    Enabled: bool = Field(True, nullable=False)


class TrendParamDef(SQLModel, table=True):
    __tablename__ = 'TrendParamDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', 'TrendDefID', name='TrendParamDef_pk'),
        {'schema': 'lds'}
    )

    ID: str = Field(sa_column=Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    TrendDefID: str = Field(sa_column=Column(
        CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
        ForeignKey('lds.TrendDef.ID'),
        nullable=False, index=True))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    DataType: str | None = Field(None, sa_column=Column(VARCHAR(6, 'SQL_Polish_CP1250_CS_AS'), nullable=True))


class Event(SQLModel, table=True):
    __tablename__ = 'Event'
    __table_args__ = (
        ForeignKeyConstraint(
            ['EventDefID'], ['lds.EventDef.ID'],
            name='Event_EventDef_fk',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        ForeignKeyConstraint(
            ['MethodID'], ['lds.Method.ID'],
            name='Event_Method_fk',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        {'schema': 'lds'}
    )

    ID: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"autoincrement": True},
    )
    EventDefID: str = (
        Field(sa_column=Column(
            CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
            nullable=False)
        ))
    MethodID: int = Field(
        sa_column=Column(
            Integer,
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
        ForeignKeyConstraint(
            ['MethodID'], ['lds.Method.ID'],
            name='MethodParam_Method_fk',
            onupdate='CASCADE',
            ondelete='CASCADE'
        ),
        {'schema': 'lds'}
    )

    MethodParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False, primary_key=True))
    MethodID: int = Field(
        sa_column=Column(
            Integer,
            nullable=False
        ))
    Value: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))


class TrendParam(base.TrendParam, table=True):
    __tablename__ = 'TrendParam'
    __table_args__ = (
        PrimaryKeyConstraint('TrendParamDefID', 'TrendID', name='TrendParam_pk'),
        {'schema': 'lds'}
    )

    TrendID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Trend.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    ))


class Template(base.Template, table=True):
    __tablename__ = 'Template'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1, increment=1), primary_key=True))


class ProfilerData(base.ProfilerData, table=True):
    __tablename__ = 'ProfilerData'
    __table_args__ = (
        {'schema': 'lds'}
    )


class SimulationDef(base.SimulationDef, table=True):
    __tablename__ = 'SimulationDef'
    __table_args__ = (
        {'schema': 'lds'}
    )


class Simulation(base.Simulation, table=True):
    __tablename__ = 'Simulation'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1, increment=1), primary_key=True))
    Enabled: bool = Field(True, nullable=False)


class SimulationParamDef(SQLModel, table=True):
    __tablename__ = 'SimulationParamDef'
    __table_args__ = (
        PrimaryKeyConstraint('ID', 'SimulationDefID', name='SimulationParamDef_pk'),
        {'schema': 'lds'}
    )

    ID: str = Field(sa_column=Column(CHAR(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    SimulationDefID: str = Field(sa_column=Column(
        CHAR(20, 'SQL_Polish_CP1250_CS_AS'),
        ForeignKey("lds.SimulationDef.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    DataType: str | None = Field(None, sa_column=Column(VARCHAR(20, 'SQL_Polish_CP1250_CS_AS'), nullable=True))


class SimulationParam(base.SimulationParam, table=True):
    __tablename__ = 'SimulationParam'
    __table_args__ = (
        PrimaryKeyConstraint('SimulationID', 'SimulationParamDefID', name='SimulationParam_pk'),
        ForeignKeyConstraint(
            ["SimulationParamDefID", "SimulationDefID"],
            ["lds.SimulationParamDef.ID", "lds.SimulationParamDef.SimulationDefID"],
            ondelete="NO ACTION", onupdate="NO ACTION"
        ),
        {'schema': 'lds'}
    )

    SimulationDefID: str = Field(sa_column=Column(
        CHAR(20, 'SQL_Polish_CP1250_CS_AS'),
        nullable=False))
    SimulationID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Simulation.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    ))


class SimulationData(base.SimulationData, table=True):
    __tablename__ = 'SimulationData'
    __table_args__ = (
        PrimaryKeyConstraint('SimulationID', 'Distance', name='SimulationData_pk'),
        {'schema': 'lds'}
    )

    SimulationID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Simulation.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    ))
    Time: int = Field(sa_column=Column(BigInteger, nullable=False))


class MethodData(SQLModel, table=True):
    __tablename__ = 'MethodData'
    __table_args__ = (
        PrimaryKeyConstraint('MethodID', 'Position', 'Time', name='MethodData_pk'),
        {'schema': 'lds'}
    )

    MethodID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Method.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    ))
    Position: int = Field(sa_column=Column(Integer, nullable=False))
    Time: int = Field(sa_column=Column(BigInteger, nullable=False))
    Value: float = Field(0.0, sa_column=Column(Float, nullable=False))
