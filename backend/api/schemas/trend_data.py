from pydantic import BaseModel, Field
from .trend_value import TrendValue


class TrendData(BaseModel):
    timestamp_ms: int = Field(alias='TimestampMs')
    timestamp: int = Field(alias='Timestamp')
    data: list[TrendValue] | None = Field(None, alias='Data')
