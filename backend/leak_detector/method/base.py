from typing import List
import logging

from sqlalchemy import select, insert, and_

from ..db import global_session, Session
from database import lds
from ..plant import Event, Plant, Trend

#Prosta Klasa segmentu, chyba można wrzucić do osobnego pliku
class Segment:
    def __init__(self, plant : Plant, start: Trend, end: Trend) -> None:
        #TO DO: Dla wielu dróg powinno wyrzucać błąd
        self._length = plant.get_distances(plant.nodes[start.node_id], plant.nodes[end.node_id])[0]
        self._start = start
        self._end = end
    
    def window_size(self, wave_speed) -> int:
        return int(self._length / wave_speed * 1000)

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

        print(stmt)

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