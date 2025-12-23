from pydantic import BaseModel, Field


class PastWriterConfig(BaseModel):
    from_timestamp: int | None = Field(None, alias='FromTimestamp')
    to_timestamp: int | None = Field(None, alias='ToTimestamp')
    quick_trend_ids: list[int] | None = Field(None, alias='QuickTrendIds')
