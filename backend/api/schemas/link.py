from decimal import Decimal

from sqlalchemy import Numeric, Column
from sqlmodel import SQLModel, Field


class LinkBase(SQLModel):
    BeginNodeID: int | None = Field(None, foreign_key='lds.Node.ID')
    EndNodeID: int | None = Field(None, foreign_key='lds.Node.ID')
    Length: Decimal | None = Field(None, sa_column=Column(Numeric(10, 2), nullable=True))


class UpdateLink(LinkBase):
    pass
