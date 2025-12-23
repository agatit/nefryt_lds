from pydantic import BaseModel, Field


class PastDetectorConfig(BaseModel):
    detection_periods: list[int] | None = Field(None, alias='DetectionPeriods')
