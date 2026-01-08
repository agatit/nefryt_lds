import logging
import numpy as np
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import Session
from database import lds
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db import get_engine
from ..plant import Event, Pipeline
from ..segment import Segment

logger = logging.getLogger(__name__)

class MethodBase:
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        self._pipeline = pipeline
        self._id = id_
        self._name = name

        self._params = {}
        self._read_params()

        logger.info(f"{self.__class__.__name__} ({self.id}): Method initialized (params={self._params})")

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

    def _get_params(self):
        pass

    def _calculate_params(self):
        pass

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

    def get_max_trend_time_delta(self) -> int:
        return 0

    def update_params(self, new_method_params: dict):
        self._params.update(new_method_params)
        self._get_params()
        self._calculate_params()
        logger.debug(f"{self.__class__.__name__} ({self.id}): Method params updated (updated params={new_method_params})")

    def _save_method_data(self, probability: np.ndarray, timestamps: range, positions: range):
        if not self._pipeline.plant.past_leak_detector:
            data_objects = []
            for row, timestamp in enumerate(timestamps):
                for column, position in enumerate(positions):
                    value = probability[row, column]
                    data_object = lds.MethodData(MethodID=self._id, Position=position, Time=timestamp, Value=value)
                    data_objects.append(data_object)

            logger.debug(f"{self.__class__.__name__} ({self.id}): Started saving {len(data_objects)} method data to database")

            with Session(get_engine()) as session:
                session.add_all(data_objects)
                session.commit()

            logger.debug(f"{self.__class__.__name__} ({self.id}): Finished saving {len(data_objects)} method data to database")

    def _delete_method_data_from_db(self):
        if not self._pipeline.plant.past_leak_detector:
            with Session(get_engine()) as session:
                session.execute(delete(lds.MethodData).where(lds.MethodData.MethodID == self.id)) # noqa
                session.commit()

            logger.debug(f"{self.__class__.__name__} ({self.id}): Removed method data from database")
