from pydantic import BaseModel, Field


class Trend(BaseModel):
    id: int | None = Field(None, alias='ID')
    trend_group_id: int | None = Field(None, alias='TrendGroupID')
    format: str | None = Field(None, alias='Format')
    symbol: str | None = Field(None, alias='Symbol')
    color: int | None = Field(None, alias='Color')
    node_id: int | None = Field(None, alias='NodeID')
    trend_def_id: str = Field(alias='TrendDefID')
    time_exponent: int | None = Field(None, alias='TimeExponent')
    unit: str | None = Field(None, alias='UnitID')
    name: str | None = Field(None, alias='Name')
    raw_min: int = Field(alias="RawMin")
    raw_max: int = Field(alias="RawMax")
    scaled_min: float = Field(alias="ScaledMin")
    scaled_max: float = Field(alias="ScaledMax")


class UpdateTrend(BaseModel):
    trend_group_id: int | None = Field(None, alias='TrendGroupID')
    format: str | None = Field(None, alias='Format')
    symbol: str | None = Field(None, alias='Symbol')
    color: int | None = Field(None, alias='Color')
    node_id: int | None = Field(None, alias='NodeID')
    trend_def_id: str | None = Field(None, alias='TrendDefID')
    time_exponent: int | None = Field(None, alias='TimeExponent')
    unit: str | None = Field(None, alias='UnitID')
    name: str | None = Field(None, alias='Name')
    raw_min: int | None = Field(None, alias="RawMin")
    raw_max: int | None = Field(None, alias="RawMax")
    scaled_min: float | None = Field(None, alias="ScaledMin")
    scaled_max: float | None = Field(None, alias="ScaledMax")
