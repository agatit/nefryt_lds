from sqlalchemy import Column, CHAR, String
from sqlmodel import SQLModel, Field


class SimulationDefBase(SQLModel):
    ID: str = Field(sa_column=Column(CHAR(20, 'SQL_Polish_CP1250_CS_AS'), primary_key=True))
    Name: str = Field(sa_column=Column(String(30, 'SQL_Polish_CP1250_CS_AS'), nullable=False))
