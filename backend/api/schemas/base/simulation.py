from sqlalchemy import Column, Integer, ForeignKey, CHAR, Float, String, SmallInteger, Identity
from sqlmodel import SQLModel, Field


class Simulation(SQLModel):
    SimulationDefID: str = Field(
        sa_column=Column(
            CHAR(20, 'SQL_Polish_CP1250_CS_AS'),
            ForeignKey("lds.SimulationDef.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False
        ))
    TrendID: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("lds.Trend.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False
        ))
    Name: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    RefreshTimeSeconds: int = Field()
    ResolutionMeters: int = Field()
