from pydantic import BaseModel


class SimulatorData(BaseModel):
    Distance: float
    Data: float | None
