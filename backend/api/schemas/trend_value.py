from pydantic import BaseModel


class TrendValue(BaseModel):
    ID: int
    Value: float | None = None
