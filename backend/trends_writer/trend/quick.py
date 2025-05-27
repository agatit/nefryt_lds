from multiprocessing.queues import Queue
from . import TrendBase


class TrendQuick(TrendBase):
    def __init__(self, _id: int, queue: Queue, db_uri: str, profiler_queue: Queue | None):
        super().__init__(_id, queue, db_uri, profiler_queue)
        self.register: int = int(float(self.params['MODBUS_REGISTER']))
