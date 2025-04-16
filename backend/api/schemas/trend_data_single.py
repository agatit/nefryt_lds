from pydantic import BaseModel, Field
from .trend_value import TrendValue


class TrendDataSingle(BaseModel):
    timestamp_ms: int = Field(alias='TimestampMs')
    timestamp: int = Field(alias='Timestamp')
    data: float = Field(alias='Value')
