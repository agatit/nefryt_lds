from typing import List
import logging

from sqlalchemy import select, insert, and_

from ..db import global_session, Session
from database import lds

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
                     

    def get_probablity(self, timestamp) -> List[float]:
        pass

    @property
    def calc_time(self) -> int:
        return self._calc_time

    @property
    def probability(self) -> List[float]:
        return self._probability