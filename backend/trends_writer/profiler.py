import atexit
import multiprocessing
import time
from trends_writer.config import Settings


class Profiler:
    queue = None
    process = None
    updates = {}
    use_profiler = False

    @staticmethod
    def init():
        if Settings.use_profiler:
            Profiler.use_profiler = True
            Profiler.queue = multiprocessing.Queue()
            Profiler.process = multiprocessing.Process(target=Profiler._process_queue, args=(Profiler.queue,))
            Profiler.process.daemon = True
            Profiler.process.start()
            atexit.register(Profiler._shutdown)

    @staticmethod
    def _process_queue(queue: multiprocessing.Queue):
        while True:
            operation, timestamp = queue.get()
            if operation == 1:
                if timestamp not in Profiler.updates:
                    Profiler.updates[timestamp] = (1, time.perf_counter())
                else:
                    count, start = Profiler.updates[timestamp]
                    Profiler.updates[timestamp] = (count + 1, start)
            elif operation == 0:
                if timestamp in Profiler.updates:
                    count, start = Profiler.updates[timestamp]
                    if count == 1:
                        time_used  = time.perf_counter() - start
                        time_used_percent = (time_used / 1.0) * 100
                        with open("profiler_queues.log", "a") as f:
                            f.write(f"Profiler: Trends writer used {time_used_percent:.2f}% of time in timestamp={timestamp}\n")
                        Profiler.updates.pop(timestamp-1, None)
                    Profiler.updates[timestamp] = (count - 1, start)
            else:
                Profiler._shutdown()
                break

    @staticmethod
    def _shutdown():
        if Profiler.process:
            Profiler.process.terminate()
            Profiler.process.join()
