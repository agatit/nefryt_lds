import logging
from typing import List

from .base import MethodBase


class MethodBalance(MethodBase):

    def __init__(self, pipeline, id, name):
        super().__init__(pipeline, id, name)
        # skopiowanie specyficznych parametrów metody:
        

    def get_probablity(self, timestamp, step) -> List[float]:
        pass    