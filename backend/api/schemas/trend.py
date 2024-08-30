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
