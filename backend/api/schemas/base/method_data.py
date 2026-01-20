from sqlalchemy import Column, Integer, BigInteger, Float
from sqlmodel import SQLModel, Field


class MethodData(SQLModel):
    Position: int = Field(sa_column=Column(Integer, nullable=False))
    Time: int = Field(sa_column=Column(BigInteger, nullable=False))
    Value: float = Field(0.0, sa_column=Column(Float, nullable=False))
