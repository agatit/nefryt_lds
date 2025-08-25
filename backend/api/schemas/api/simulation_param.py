from sqlmodel import Field
from ...schemas import base


class SimulationParam(base.SimulationParam):
    SimulationID: int
    DataType: str | None = Field(None)
    Name: str | None = Field(None)
    Value: str | None = Field(None)


class SimulationParamCreate(base.SimulationParam):
    pass
