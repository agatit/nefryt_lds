from sqlalchemy import Column, CHAR, VARCHAR
from sqlmodel import Field
from ...schemas import base


class Event(base.Event):
    Verbosity: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Caption: str = Field(sa_column=Column(VARCHAR(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Silent: bool = Field(default=False, nullable=False)
