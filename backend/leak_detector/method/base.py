import logging
from math import ceil
from typing import List

from sqlalchemy import select, and_

from ..db import global_session
from database import lds
from ..plant import Event, Pipeline

# Zakładamy, że:
# Jeden wspólny pipeline dla metody, bo składanie metod się nie uda ze względu na możliwe różnice wielkości step'ów.
class MethodBase:
    def __init__(self, pipeline: Pipeline, id: int, name: str):
        self._pipeline = pipeline
        self._id = id
        self._name = name

        self._params = {}
        self._read_params()

        logging.info(f"Method {id}: {name} created.")


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
                     

    def get_probability(self, begin: int, end: int) -> List[List[float]]:
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