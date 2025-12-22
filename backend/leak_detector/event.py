from datetime import datetime
import logging
from sqlalchemy.orm import Session
from database import lds
from db import get_engine

logger = logging.getLogger(__name__)


class Event:
    def __init__(self, method_id: int, time: int, position: float) -> None:
        self.method_id = method_id
        self._time = time
        self._datetime = datetime.fromtimestamp(time / 1000)
        self._position = position
        logger.debug(f"Event: Created for method with id = {self.method_id} with params {self._datetime}, {self._position}m")

    def save(self) -> None:
        event = lds.Event(EventDefID='LEAK',
            MethodID=self.method_id,
            BeginDate=self.datetime,
            Position=self.position)

        with Session(get_engine()) as session:
            session.add(event)
            session.commit()
        logger.debug(f"Saved leak event for method with id = {self.method_id} with params {self._datetime}, {self._position}m")

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @property
    def position(self) -> float:
        return self._position

    @property
    def time(self) -> int:
        return self._time

    def __str__(self):
        return f'position: {self.position}, time: {self._datetime}'

    def __repr__(self):
        return str(self)
