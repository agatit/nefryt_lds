from sqlalchemy import Column, Integer, ForeignKey, CHAR, Float, String
from sqlmodel import SQLModel, Field


class Trend(SQLModel):
    TrendDefID: str = Field(
        sa_column=Column(
            CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
            nullable=False))
    RawMin: int = Field()
    RawMax: int = Field()
    ScaledMin: float = Field(sa_column=Column(Float(53), nullable=False))
    ScaledMax: float = Field(sa_column=Column(Float(53), nullable=False))
    Name: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    TrendGroupID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.TrendGroup.ID", onupdate="CASCADE"),
        nullable=False
    ))
    TimeExponent: int | None = Field(None)
    Format: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    UnitID: str = Field(sa_column=Column(
        CHAR(10, 'SQL_Polish_CP1250_CS_AS'),
        ForeignKey('lds.Unit.ID'),
        nullable=False
    ))
    Color: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Symbol: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    NodeID: int | None = Field(None,
                               sa_column=Column(
                                   Integer,
                                   ForeignKey("lds.Node.ID", ondelete='SET NULL'),
                                   nullable=True))
    TimeDelta: int = Field(0)
