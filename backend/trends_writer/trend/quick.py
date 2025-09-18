from multiprocessing.queues import Queue
from . import TrendBase


class TrendQuick(TrendBase):
    def __init__(self, id_: int, queue: Queue, db_uri: str, profiler_queue: Queue):
        super().__init__(id_, queue, db_uri, profiler_queue)
        self.register: int = int(float(self.params['MODBUS_REGISTER']))
