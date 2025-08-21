from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field


class SimulationParam(SQLModel):
    Value: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS')))
