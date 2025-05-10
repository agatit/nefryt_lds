from multiprocessing.queues import Queue
from . import TrendBase


class TrendQuick(TrendBase):
    def __init__(self, _id: int, queue: Queue, profiler_queue: Queue | None):
        super().__init__(_id, queue, profiler_queue)
        self.register: int = int(float(self.params['MODBUS_REGISTER']))
        self.start_process_queue()
