from sqlmodel import Field
from ...schemas import base


class PipelineParam(base.PipelineParam):
    PipelineID: int
    DataType: str | None = Field(None)
    Name: str | None = Field(None)
    Value: str | None = Field(None)


class PipelineParamCreate(base.PipelineParam):
    pass
