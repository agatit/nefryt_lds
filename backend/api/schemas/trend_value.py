from pydantic import Field, BaseModel


class TrendValue(BaseModel):
    id: int = Field(alias='ID')
    value: float | None = Field(None, alias='Value')
