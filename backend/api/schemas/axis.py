from pydantic import BaseModel, Field


class Axis(BaseModel):
    TrendsID: list[int] = Field([])
    Title: str = Field()
    Unit: str = Field()
    ScaledMin: float = Field()
    ScaledMax: float = Field()
