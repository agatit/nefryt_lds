from sqlalchemy import Column, CHAR
from sqlmodel import SQLModel, Field


class EventDefBase(SQLModel):
    Verbosity: str = Field(sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Caption: str = Field(sa_column=Column(CHAR(60, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
    Silent: bool = Field(default=False, nullable=False)
    Visible: bool = Field(default=True, nullable=False)
    Enabled: bool = Field(default=True, nullable=False)


class UpdateEventDef(SQLModel):
    Verbosity: str | None = Field(None, sa_column=Column(CHAR(10, 'SQL_Polish_CP1250_CS_AS')))
    Caption: str | None = Field(None, sa_column=Column(CHAR(60, 'SQL_Polish_CP1250_CS_AS')))
    Silent: bool | None = Field(None)
    Visible: bool | None = Field(None)
    Enabled: bool | None = Field(None)
