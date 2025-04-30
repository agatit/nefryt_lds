import atexit
import multiprocessing
import threading
import time


class Profiler:
    use_asyncio = None
    queue = None
    process = None
    updates = {}
    lock = None

    @staticmethod
    def init(use_asyncio=True):
        Profiler.use_asyncio = use_asyncio
        if Profiler.use_asyncio:
            Profiler.queue = multiprocessing.Queue()
            Profiler.process = multiprocessing.Process(target=Profiler._process_queue, args=(Profiler.queue,))
            Profiler.process.daemon = True
            Profiler.process.start()
            atexit.register(Profiler._shutdown)
        else:
            Profiler.lock = threading.Lock()

    @staticmethod
    def add_update(timestamp):
        if Profiler.use_asyncio:
            Profiler.queue.put((1, timestamp))
        else:
            with Profiler.lock:
                if timestamp not in Profiler.updates:
                    Profiler.updates[timestamp] = (1, time.perf_counter())
                else:
                    count, start = Profiler.updates[timestamp]
                    Profiler.updates[timestamp] = (count + 1, start)

    @staticmethod
    def remove_update(timestamp):
        if Profiler.use_asyncio:
            Profiler.queue.put((0, timestamp))
        else:
            with Profiler.lock:
                if timestamp in Profiler.updates:
                    count, start = Profiler.updates[timestamp]
                    if count == 1:
                        time_used  = time.perf_counter() - start
                        time_used_percent = (time_used / 1.0) * 100
                        with open("profiler_threading.log", "a") as f:
                            f.write(f"Profiler: Trends writer used {time_used_percent:.2f}% of time in timestamp={timestamp}\n")
                        Profiler.updates.pop(timestamp-1, None)
                    Profiler.updates[timestamp] = (count - 1, start)

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
            else:
                if timestamp in Profiler.updates:
                    count, start = Profiler.updates[timestamp]
                    if count == 1:
                        time_used  = time.perf_counter() - start
                        time_used_percent = (time_used / 1.0) * 100
                        with open("profiler_asyncio.log", "a") as f:
                            f.write(f"Profiler: Trends writer used {time_used_percent:.2f}% of time in timestamp={timestamp}\n")
                        Profiler.updates.pop(timestamp-1, None)
                    Profiler.updates[timestamp] = (count - 1, start)

    @staticmethod
    def _shutdown():
        if Profiler.process:
            Profiler.process.terminate()
            Profiler.process.join()
