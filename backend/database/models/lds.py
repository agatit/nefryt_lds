from datetime import datetime
from sqlalchemy import BINARY, BigInteger, CHAR, Column, Identity, \
    Integer, Numeric, PrimaryKeyConstraint, String, ForeignKey, VARCHAR, ForeignKeyConstraint, Index
from sqlmodel import SQLModel, Field
from api.schemas import EventDefBase, LdsNodeBase, LinkBase, TrendDefBase, TrendBase, TrendParamBase, TemplateBase, \
    UnitBase


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


class Pipeline(SQLModel, table=True):
    __tablename__ = 'Pipeline'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=2, increment=1), primary_key=True))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    BeginPos: float | None = Field(None, sa_column=Column(Numeric(10, 2), nullable=True))


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


class TrendDef(TrendDefBase, table=True):
    __tablename__ = 'TrendDef'
    __table_args__ = (
        {'schema': 'lds'}
    )


class TrendGroup(SQLModel, table=True):
    __tablename__ = 'TrendGroup'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1, increment=1), primary_key=True, nullable=False))
    Name: str = Field(sa_column=Column(String(100, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    AnalysisOnly: bool = Field(False, nullable=False, sa_column_kwargs={"server_default": "0"})


class Unit(UnitBase, table=True):
    __tablename__ = 'Unit'
    __table_args__ = (
        {'schema': 'lds'}
    )


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


class PipelineParam(SQLModel, table=True):
    __tablename__ = 'PipelineParam'
    __table_args__ = (
        PrimaryKeyConstraint('PipelineParamDefID', 'PipelineID', name='PipelineParam_pk'),
        {'schema': 'lds'}
    )

    PipelineParamDefID: str = Field(
        sa_column=Column(
            CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
            ForeignKey("lds.PipelineParamDef.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False))
    PipelineID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("lds.Pipeline.ID"),
            nullable=False
        )
    )
    Value: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))


class Trend(TrendBase, table=True):
    __tablename__ = 'Trend'
    __table_args__ = (
        ForeignKeyConstraint(
            ['TrendDefID'], ['lds.TrendDef.ID'],
            name='Trend_TrendDef_fk',
            ondelete='CASCADE'
        ),
        {'schema': 'lds'}
    )


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
        sa_type=BigInteger
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


class TrendParam(TrendParamBase, table=True):
    __tablename__ = 'TrendParam'
    __table_args__ = (
        PrimaryKeyConstraint('TrendParamDefID', 'TrendID', name='TrendParam_pk'),
        {'schema': 'lds'}
    )


class Template(TemplateBase, table=True):
    __tablename__ = 'Template'
    __table_args__ = (
        {'schema': 'lds'}
    )

    ID: int = Field(sa_column=Column(Integer, Identity(start=1, increment=1), primary_key=True))
