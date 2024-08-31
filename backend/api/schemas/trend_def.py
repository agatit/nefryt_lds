from pydantic import BaseModel, Field


class TrendDef(BaseModel):
    id: str = Field(alias='ID')
    name: str = Field(alias='Name')
