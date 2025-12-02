import logging
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from database import lds
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db import get_engine
from ..plant import Event, Pipeline
from ..segment import Segment

class MethodBase:
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        self._pipeline = pipeline
        self._id = id_
        self._name = name

        self._params = {}
        self._read_params()

        logging.debug(f"Method {id_}: {name} created.")

    def _read_params(self):
        statement = (select(lds.MethodParam)
                     .select_from(lds.Method)
                     .join(lds.MethodDef, lds.Method.MethodDefID == lds.MethodDef.ID)  # noqa
                     .join(lds.MethodParamDef, lds.MethodDef.ID == lds.MethodParamDef.MethodDefID)
                     .join(lds.MethodParam, and_(lds.MethodParamDef.ID == lds.MethodParam.MethodParamDefID,
                                                 lds.Method.ID == lds.MethodParam.MethodID))
                     .where(lds.Method.ID == self._id))

        with Session(get_engine()) as session:
            method_params = session.scalars(statement).all()
        for mp in method_params:
            self._params[mp.MethodParamDefID.strip()] = mp.Value

    def get_probability(self, segment: Segment, begin: int, end: int) -> list[list[float]]:
        pass

    def find_leaks_in_range(self, begin: int, end: int) -> list[Event]:
        pass

    def find_leaks_to(self, end: int) -> list[Event]:
        pass

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline

    @property
    def id(self) -> int:
        return self._id

    def get_leakage_alarm_delta(self) -> int:
        return 0
