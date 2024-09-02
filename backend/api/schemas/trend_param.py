from pydantic import BaseModel, Field


class TrendParam(BaseModel):
    trend_id: int = Field(alias='TrendID')
    value: str = Field(alias='Value')
    trend_param_def_id: str = Field(alias='TrendParamDefID')
    data_type: str | None = Field(None, alias='DataType')
    name: str | None = Field(None, alias='Name')
