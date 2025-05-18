from multiprocessing import Process
from multiprocessing.queues import Queue
import numpy as np
from . import TrendBase
from ..config import setup_engine, Settings
from ..profiler import Profiler


class TrendQuick(TrendBase):
    def __init__(self, _id: int, queue: Queue):
        super().__init__(_id)
        self.register: int = int(float(self.params['MODBUS_REGISTER']))
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
