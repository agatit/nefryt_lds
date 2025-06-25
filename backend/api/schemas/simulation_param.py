from pydantic import BaseModel
from sqlalchemy import CHAR, Column, String, ForeignKey, Integer
from sqlmodel import SQLModel, Field


class SimulationParamBase(SQLModel):
    SimulationID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Simulation.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    ))
    SimulationParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
        nullable=False))
    Value: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS')))


class SimulationParamOut(SimulationParamBase):
    DataType: str = Field()
    Name: str = Field()


class UpdateSimulationParam(BaseModel):
    SimulationID: int | None = Field(None, sa_column=Column(
        Integer,
        ForeignKey("lds.Simulation.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True
    ))
    SimulationParamDefID: str | None = Field(None, sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
        nullable=True))
    Value: str | None = Field(None, sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS')))


class SimulationParamIn(SQLModel):
    SimulationParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
        nullable=False))
    Value: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS')))
