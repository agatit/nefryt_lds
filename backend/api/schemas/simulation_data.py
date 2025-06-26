from pydantic import BaseModel
from sqlalchemy import Integer
from sqlmodel import SQLModel, Field


class SimulationDataBase(SQLModel):
    Distance: int = Field(Integer)
    Data: int | None = Field(Integer)


class SimulationDataOut(BaseModel):
    SimulationID: int = Field()
    Time: int = Field()
    Data: list[SimulationDataBase] = Field([])
