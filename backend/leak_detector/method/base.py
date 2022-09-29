import logging
from math import ceil
from typing import List

from sqlalchemy import select, and_

from ..db import global_session
from database import lds
from ..plant import Event, Pipeline
from ..trend import Trend

class Segment:
    def __init__(self, pipeline: Pipeline, start: Trend, end: Trend, begin_pos: int, wave_speed: float) -> None:
        distances = pipeline.plant.get_distances(pipeline.plant.nodes[start.node_id], pipeline.plant.nodes[end.node_id])
        if (len(distances) != 1):
            logging.exception(f"There isn't exactly one path between {start.id} and {end.id}.")
            raise
        self._length = distances[0]
        self._start = start
        self._end = end
        self._begin_pos = begin_pos
        self._end_pos = self._begin_pos + self._length
        self._wave_speed = wave_speed
        self._max_window_size = ceil(self._length / self._wave_speed) * 1000

        logging.debug(f"Segment {start.id} <--> {end.id} created.")

    # TODO:
    # - Liczenie wave_speed dla danego punktu na segmencie pipeline'u.
    def calc_wave_speed(self) -> float:
        return self._wave_speed

    @property
    def max_window_size(self) -> int:
        return self._max_window_size


# Zakładamy, że:
# Jeden wspólny pipeline dla metody, bo składanie metod się nie uda ze względu na możliwe różnice wielkości step'ów.
class MethodBase:
    def __init__(self, pipeline: Pipeline, id: int, name: str):
        self._pipeline = pipeline
        self._id = id
        self._name = name

        self._params = {}
        self._read_params()

        logging.debug(f"Method {id}: {name} created.")


    def _read_params(self):
        stmt = select([lds.MethodParam]) \
            .select_from(lds.Method) \
            .join(lds.MethodDef, lds.Method.MethodDefID == lds.MethodDef.ID) \
            .join(lds.MethodParamDef, lds.MethodDef.ID == lds.MethodParamDef.MethodDefID) \
            .join(lds.MethodParam, and_(lds.MethodParamDef.ID == lds.MethodParam.MethodParamDefID, lds.Method.ID == lds.MethodParam.MethodID)) \
            .where(lds.Method.ID == self._id)
        logging.debug(stmt)

        self._params = {}
        for param, in global_session.execute(stmt):
            self._params[param.MethodParamDefID.strip()] = param.Value   
                     

    def get_probability(self, segment: Segment, begin: int, end: int) -> List[List[float]]:
        pass


    def find_leaks_in_range(self, begin: int, end: int) -> List[Event]:
        """ Po przemyśleniu wydaje mi się, że cały mechanizm powinien być zaimplementowany
            na poziomie metody, gdyż lokalizacja zdarzenia będzie nieco inna dla róznych metod.
            Implementacja na poziomie pipelinu powinna tylko skaładać wyniki z metod w jeden
        """
        pass


    def find_leaks_to(self, end: int) -> List[Event]:
        """ j.w.
        """
        pass  

    @property
    def calc_time(self) -> int:
        return self._calc_time

    @property
    def probability(self) -> List[float]:
        return self._probability