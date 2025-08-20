from typing import Sequence
from pydantic import BaseModel, Field

class TrendDataSingle(BaseModel):
    timestamp_ms: int = Field(alias='TimestampMs')
    timestamp: int = Field(alias='Timestamp')
    data: float = Field(alias='Value')


class TrendValue(BaseModel):
    ID: int
    Value: float | None = None


class TrendDataMultiple(BaseModel):
    TimestampMs: int
    Timestamp: int
    Data: list[TrendValue | None] | None = None


class CurrentTrendData(BaseModel):
    LastTimestamp: int
    Data: list[TrendDataMultiple] | Sequence[TrendDataMultiple] = []
