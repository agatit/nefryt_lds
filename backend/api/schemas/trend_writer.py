from pydantic import BaseModel
from sqlalchemy import Column, Integer, ForeignKey
from sqlmodel import SQLModel, Field


class ProfilerDataBase(SQLModel):
    ID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Trend.ID", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=True
    ))
    Time10: float | None = Field(None, nullable=True)
    Time100: float | None = Field(None, nullable=True)
    Time1000: float | None = Field(None, nullable=True)
    QueueSize: int | None = Field(None, nullable=True)


class ProfilerGeneralData(BaseModel):
    ActiveTrends: int = Field(0)
    Time10: float = Field(0)
    Time100: float = Field(0)
    Time1000: float = Field(0)
    QueueSize: float = Field(0)
