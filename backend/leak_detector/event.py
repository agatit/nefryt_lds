from datetime import datetime
import logging

from sqlalchemy import insert
from sqlalchemy.orm import Session

from database import lds
from db import get_engine


class Event:
    def __init__(self, method_id: int, time: int, position: float) -> None:
        self.method_id = method_id
        self._datetime = datetime.fromtimestamp(time / 1000)
        self._position = position
        logging.debug(f"Event {method_id}: {self._datetime} {position}m created.")

    # TODO:
    # - Zapisywanie event'ów.
    def save(self) -> None:
        stmt = insert(lds.Event).values(
            EventDefID='LEAK',
            MethodID=self.method_id,
            BeginDate=self.datetime,
            Position=self.position
        )
        with Session(get_engine()) as session:
            logging.debug(stmt)
            session.execute(stmt)
            session.commit()
        return

    @property
    def datetime(self) -> datetime:
        return self._datetime

    @property
    def position(self) -> float:
        return self._position
