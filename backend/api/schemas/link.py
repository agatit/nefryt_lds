from sqlmodel import SQLModel, Field


class LinkBase(SQLModel):
    BeginNodeID: int | None = Field(None, foreign_key='lds.Node.ID')
    EndNodeID: int | None = Field(None, foreign_key='lds.Node.ID')
    Length: float | None = Field(None)


class UpdateLink(LinkBase):
    pass
