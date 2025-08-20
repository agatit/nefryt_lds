from sqlalchemy import Column, CHAR, VARCHAR
from sqlmodel import SQLModel, Field


class EventDef(SQLModel):
    Verbosity: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Caption: str = Field(sa_column=Column(VARCHAR(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Silent: bool = Field(default=False, nullable=False, sa_column_kwargs={"server_default": "0"})
    Visible: bool = Field(default=True, nullable=False, sa_column_kwargs={"server_default": "1"})
    Enabled: bool = Field(default=True, nullable=False, sa_column_kwargs={"server_default": "1"})
