from sqlalchemy import Column, Integer, ForeignKey, DECIMAL
from sqlmodel import SQLModel, Field


class ProfilerData(SQLModel):
    ID: int = Field(sa_column=Column(
        Integer,
        ForeignKey("lds.Trend.ID", onupdate="CASCADE", ondelete="CASCADE"),
        primary_key=True,
        nullable=False
    ))
    Time10: float | None = Field(
        default=None,
        sa_column=Column(DECIMAL(10, 5), nullable=True)
    )
    Time100: float | None = Field(
        default=None,
        sa_column=Column(DECIMAL(10, 5), nullable=True)
    )
    Time1000: float | None = Field(
        default=None,
        sa_column=Column(DECIMAL(10, 5), nullable=True)
    )
    QueueSize: int | None = Field(None, nullable=True)
