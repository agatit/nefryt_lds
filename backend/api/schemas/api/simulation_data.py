from pydantic import BaseModel
from sqlmodel import Field
from ...schemas import base


class SimulationData(BaseModel):
    SimulationID: int = Field()
    Time: int = Field()
    Data: list[base.SimulationData] = Field([])
