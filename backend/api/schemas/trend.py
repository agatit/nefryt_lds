from sqlalchemy import Column, Integer, ForeignKey, CHAR, Float, String, SmallInteger, Identity
from sqlmodel import SQLModel, Field


class TrendBase(SQLModel):
    ID: int = Field(sa_column=Column(Integer, Identity(start=1000, increment=1), nullable=False, primary_key=True))
    TrendDefID: str = Field(
        sa_column=Column(
            CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
            nullable=False))
    RawMin: int = Field()
    RawMax: int = Field()
    ScaledMin: float = Field(sa_column=Column(Float(53), nullable=False))
    ScaledMax: float = Field(sa_column=Column(Float(53), nullable=False))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    TrendGroupID: int | None = Field(None)
    TimeExponent: int | None = Field(None)
    Format: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    UnitID: str | None = Field(None,
                               sa_column=Column(
                                   CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
                                   ForeignKey('lds.Unit.ID'),
                                   nullable=True))
    Color: int | None = Field(None, sa_column=Column(SmallInteger, nullable=True))
    Symbol: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    NodeID: int | None = Field(None,
                               sa_column=Column(
                                   Integer,
                                   ForeignKey("lds.Node.ID", ondelete='SET NULL'),
                                   nullable=True))


class UpdateTrend(SQLModel):
    TrendDefID: str | None = Field(None,
                                   sa_column=Column(
                                       CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
                                       ForeignKey("lds.TrendDef.ID", ondelete="CASCADE"),
                                       nullable=False))
    RawMin: int | None = Field(None)
    RawMax: int | None = Field(None)
    ScaledMin: float | None = Field(None, sa_column=Column(Float(53), nullable=False))
    ScaledMax: float | None = Field(None, sa_column=Column(Float(53), nullable=False))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    TrendGroupID: int | None = Field(None)
    TimeExponent: int | None = Field(None)
    Format: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    UnitID: str | None = Field(None,
                               sa_column=Column(
                                   CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
                                   ForeignKey('lds.Unit.ID'),
                                   nullable=True))
    Color: int | None = Field(None, sa_column=Column(SmallInteger, nullable=True))
    Symbol: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    NodeID: int | None = Field(None,
                               sa_column=Column(
                                   Integer,
                                   ForeignKey("lds.Node.ID", ondelete='SET NULL'),
                                   nullable=True))
