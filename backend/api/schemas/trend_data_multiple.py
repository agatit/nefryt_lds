from pydantic import BaseModel, Field
from .trend_value import TrendValue


class TrendDataMultiple(BaseModel):
    timestamp_ms: int = Field(alias='TimestampMs')
    timestamp: int = Field(alias='Timestamp')
    data: list[TrendValue | None] | None = Field(None, alias='Data')
