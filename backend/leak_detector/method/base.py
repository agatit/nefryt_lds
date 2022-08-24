from math import ceil
from typing import List
import logging

from sqlalchemy import select, and_

from ..db import global_session
from database import lds
from ..plant import Event, Trend, Pipeline

class Segment:
    # Na razie jest, że każdy segment ma stały wave_speed

    def __init__(self, pipeline : Pipeline, start: Trend, end: Trend, begin_pos, wave_speed) -> None:
        #TO DO: Dla wielu dróg powinno wyrzucać błąd
        distances = pipeline.plant.get_distances(pipeline.plant.nodes[start.node_id],
                                                 pipeline.plant.nodes[end.node_id])
        self._length = distances[0]
        self._start = start
        self._end = end
        self._begin_pos = begin_pos
        self._end_pos = self._begin_pos + self._length



        # Tutaj maksymalne okno powinno zostać policzone w inny sposób,
        # jeżeli segment nie będzie miał stałego wave_speed
        self._wave_speed = wave_speed
        self._max_window_size = ceil(self._length / self._wave_speed) * 1000 


    def calc_wave_speed(self, position) -> int:
        return self._wave_speed


    @property
    def max_window_size(self) -> int:
        return self._max_window_size

    @property
    def length(self) -> int:
        return self._length
    
    @property
    def start(self) -> Trend:
        return self._start
    
    @property
    def end(self) -> Trend:
        return self._end

class MethodBase:
    def __init__(self, pipeline, id, name):

        self._pipeline = pipeline # jeden wspólny step dla całego pipline, inaczej utkniemy na składaniu.
        self._id = id
        self._name = name

        # wynik obliczeń poiwnien być przechowywany, żeby nie musieć ponownego obliczania gdy inna metoda opiera się na tej
        self._probability = []
        self._calc_time = 0

        self._params = {}
        self._read_params()


    def _read_params(self):
        stmt = select([lds.MethodParam]) \
            .select_from(lds.Method) \
            .join(lds.MethodDef, lds.Method.MethodDefID == lds.MethodDef.ID) \
            .join(lds.MethodParamDef, lds.MethodDef.ID == lds.MethodParamDef.MethodDefID) \
            .join(lds.MethodParam, and_(lds.MethodParamDef.ID == lds.MethodParam.MethodParamDefID, lds.Method.ID == lds.MethodParam.MethodID)) \
            .where(lds.Method.ID == self._id)

        self._params = {}
        for param, in global_session.execute(stmt):
            self._params[param.MethodParamDefID.strip()] = param.Value   
                     

    def get_probability(self, begin, end) -> List[List[float]]:
        pass


    def find_leaks_in_range(self, begin, end) -> List[Event]:
        """ Po przemyśleniu wydaje mi się, że cały mechanizm powinien być zaimplementowany
            na poziomie metody, gdyż lokalizacja zdarzenia będzie nieco inna dla róznych metod.
            Implementacja na poziomie pipelinu powinna tylko skaładać wyniki z metod w jeden
        """
        pass


    def find_leaks_to(self, end) -> List[Event]:
        """ j.w.
        """
        pass  

    @property
    def calc_time(self) -> int:
        return self._calc_time

    @property
    def probability(self) -> List[float]:
        return self._probability