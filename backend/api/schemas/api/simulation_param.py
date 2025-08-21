from sqlalchemy import Column, Integer, ForeignKey, CHAR, String
from sqlmodel import Field
from ...schemas import base


class SimulationParam(base.SimulationParam):
    SimulationID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Simulation.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    ))
    SimulationParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
        nullable=False))
    DataType: str = Field()
    Name: str = Field()


class SimulationParamCreate(base.SimulationParam):
    SimulationParamDefID: str = Field(sa_column=Column(
        CHAR(30, 'SQL_Polish_CP1250_CS_AS'),
        nullable=False))
