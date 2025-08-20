from pydantic import BaseModel
from ...schemas import base


class ProfilerGeneralData(BaseModel):
    ActiveTrends: int = 0
    Time10: float = 0
    Time100: float = 0
    Time1000: float = 0
    QueueSize: float = 0


class ProfilerData(base.ProfilerData):
    pass
