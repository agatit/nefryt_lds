from multiprocessing import Process
from multiprocessing.queues import Queue
import numpy as np
from . import TrendBase
from ..config import setup_engine, Settings
from ..profiler import Profiler
import logging

logger = logging.getLogger(__name__)


class TrendQuick(TrendBase):

    def __init__(self, id: int, queue: Queue, parent_id: int = None):
        super().__init__(id, parent_id)
        self.register: int = int(self.params['MODBUS_REGISTER'])
        self.queue = queue
        self.process = Process(target=self.process_queue, args=(queue, Profiler.queue, Settings.db_uri))
        self.process.start()

    def process_queue(self, queue: Queue, profiler_queue: Queue | None, db_uri: str):
        setup_engine(db_uri)
        while True:
            item = queue.get()
            if item is None:
                break
            self.update(np.array(item[0]), item[1])
            if profiler_queue:
                profiler_queue.put((0, item[1]))
