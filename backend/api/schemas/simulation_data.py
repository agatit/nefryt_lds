from pydantic import BaseModel
from sqlmodel import SQLModel, Field


class SimulationDataBase(SQLModel):
    Distance: float = Field()
    Data: int | None = Field(None)


class SimulationDataOut(BaseModel):
    SimulationID: int = Field()
    Time: int = Field()
    Data: list[SimulationDataBase] = Field([])
