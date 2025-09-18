from .base import MethodBase
from ..plant import Pipeline
from ..segment import Segment


class MethodCombine(MethodBase):
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        super().__init__(pipeline, id_, name)

    def get_probability(self, segment: Segment, begin: int, end: int) -> list[list[float]]:
        pass
