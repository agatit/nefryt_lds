from pydantic import BaseModel
from .trend_value import TrendValue


class TrendDataMultiple(BaseModel):
    TimestampMs: int
    Timestamp: int
    Data: list[TrendValue | None] | None = None
