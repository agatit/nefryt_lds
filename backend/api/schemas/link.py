from pydantic import BaseModel, Field


class Link(BaseModel):
    id: int | None = Field(None, alias='ID')
    begin_node_id: int | None = Field(None, alias='BeginNodeID')
    end_node_id: int | None = Field(None, alias='EndNodeID')
    length: float | None = Field(None, alias='Length')


class UpdateLink(BaseModel):
    begin_node_id: int | None = Field(None, alias='BeginNodeID')
    end_node_id: int | None = Field(None, alias='EndNodeID')
    length: float | None = Field(None, alias='Length')
