from sqlalchemy import Column, Integer, ForeignKey, CHAR, Float, String, SmallInteger
from sqlmodel import Field
from ...schemas import base


class TrendCreate(base.Trend):
    pass


class TrendUpdate(base.Trend):
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
    Color: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Symbol: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    NodeID: int | None = Field(None,
                               sa_column=Column(
                                   Integer,
                                   ForeignKey("lds.Node.ID", ondelete='SET NULL'),
                                   nullable=True))
