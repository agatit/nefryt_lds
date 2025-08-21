from sqlmodel import SQLModel, Field


class SimulationData(SQLModel):
    Distance: float = Field()
    Data: int | None = Field(None)
