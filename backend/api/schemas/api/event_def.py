from sqlalchemy import Column, CHAR
from sqlmodel import Field
from .. import base


class EventDefCreate(base.EventDef):
    ID: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), primary_key=True))


class EventDefUpdate(base.EventDef):
    Verbosity: str | None = Field(None, sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS')))
    Caption: str | None = Field(None, sa_column=Column(CHAR(60, 'SQL_Polish_CP1250_CS_AS')))
    Silent: bool | None = Field(None)
    Visible: bool | None = Field(None)
    Enabled: bool | None = Field(None)
