from pydantic import BaseModel, Field


class EventDef(BaseModel):
    id: str | None = Field(None, alias='ID')
    verbosity: str | None = Field(None, alias='Verbosity')
    caption: str | None = Field(None, alias='Caption')
    silent: bool | None = Field(None, alias='Silent')
    visible: bool | None = Field(None, alias='Visible')
    enabled: bool | None = Field(None, alias='Enabled')
