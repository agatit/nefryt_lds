from pydantic import BaseModel, Field


class EditorNode(BaseModel):
    pos_x: int = Field(None, alias='PosX')
    pos_y: int = Field(None, alias='PosY')


class Node(BaseModel):
    id: int | None = Field(None, alias='ID')
    type: str = Field(alias='Type')
    trend_id: int | None = Field(None, alias='TrendID')
    name: str | None = Field(None, alias='Name')
    editor_params: EditorNode | None = Field(None, alias='EditorParams')


class UpdateNode(BaseModel):
    type: str = Field(alias='Type')
    trend_id: int | None = Field(None, alias='TrendID')
    name: str | None = Field(None, alias='Name')
    editor_params: EditorNode | None = Field(None, alias='EditorParams')
