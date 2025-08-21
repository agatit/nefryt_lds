from sqlalchemy import Column, Integer, ForeignKey, CHAR, String
from sqlmodel import Field
from ...schemas import base


class SimulationCreate(base.Simulation):
    pass


class SimulationUpdate(base.Simulation):
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
    ResolutionMeters: int | None = Field(None)
