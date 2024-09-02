from pydantic import BaseModel, Field


class TrendData(BaseModel):
    timestamp_ms: int = Field(alias='TimestampMs')
    timestamp: int = Field(alias='Timestamp')
