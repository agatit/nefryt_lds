from datetime import datetime
from pydantic import BaseModel, Field


class Event(BaseModel):
    id: int | None = Field(None, alias='ID')
    method_id: int = Field(alias='MethodID')
    details: str | None = Field(None, alias='Details')
    position: int | None = Field(None, alias='Position')
    event_def_id: str = Field(alias='EventDefID')
    verbosity: str | None = Field(None, alias='Verbosity')
    caption: str | None = Field(None, alias='Caption')
    silent: bool | None = Field(None, alias='Silient')
    begin_date: datetime = Field(alias='BeginDate')
    ack_date: datetime | None = Field(None, alias='AckDate')
    end_date: datetime | None = Field(None, alias='EndDate')
