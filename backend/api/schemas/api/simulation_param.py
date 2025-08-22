from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import Field
from ...schemas import base


class SimulationParam(base.SimulationParam):
    SimulationID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Simulation.ID", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    ))
    DataType: str | None = Field()
    Name: str | None = Field()
    Value: str | None = Field()


class SimulationParamCreate(base.SimulationParam):
    pass
