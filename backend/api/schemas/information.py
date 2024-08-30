from pydantic import BaseModel


class Information(BaseModel):
    message: str
    affected: int
    status: int
