from pydantic import BaseModel, Field


class Axis(BaseModel):
    TrendsID: list[int] = Field([])
    Unit: str = Field()
    ScaledMin: float = Field()
    ScaledMax: float = Field()
