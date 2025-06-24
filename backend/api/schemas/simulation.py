from sqlalchemy import Column, Integer, ForeignKey, CHAR, Float, String, SmallInteger, Identity
from sqlmodel import SQLModel, Field


class SimulationBase(SQLModel):
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
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    RefreshTimeSeconds: int = Field()
    DistanceMeters: int = Field()



class UpdateSimulation(SQLModel):
    SimulationDefID: str | None = Field(None,
        sa_column=Column(
            CHAR(20, 'SQL_Polish_CP1250_CS_AS'),
            ForeignKey("lds.SimulationDef.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=True
        ))
    TrendID: int | None = Field(None,
        sa_column=Column(
            Integer,
            ForeignKey("lds.Trend.ID", ondelete="CASCADE", onupdate="CASCADE"),
            nullable=True
        ))
    Name: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=True))
    RefreshTimeSeconds: int | None = Field(None)
    DistanceMeters: int | None = Field(None)

