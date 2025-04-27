from pydantic import BaseModel, Field


class TrendDataSingle(BaseModel):
    timestamp_ms: int = Field(alias='TimestampMs')
    timestamp: int = Field(alias='Timestamp')
    data: float = Field(alias='Value')
