from typing import Sequence
from pydantic import BaseModel
from . import TrendDataMultiple


class CurrentTrendData(BaseModel):
    LastTimestamp: int
    Data: list[TrendDataMultiple] | Sequence[TrendDataMultiple] = []
