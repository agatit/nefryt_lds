import atexit
import multiprocessing
import time
from trends_writer.config import Settings


class Profiler:
    queue = None
    process = None
    updates = {}
    use_profiler = False
    buffer = 5

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
                    Profiler.updates[timestamp] = (1, time.perf_counter(), 0)
                else:
                    count, start, time_used = Profiler.updates[timestamp]
                    if count > 0:
                        Profiler.updates[timestamp] = (count + 1, start, time_used)
                    else:
                        Profiler.updates[timestamp] = (1, time.perf_counter(), time_used)
            elif operation == 0:
                if timestamp in Profiler.updates:
                    count, start, time_used = Profiler.updates[timestamp]
                    if count == 1:
                        time_used  += time.perf_counter() - start
                        profiler_data: tuple | None = Profiler.updates.pop(timestamp-Profiler.buffer, None)
                        if profiler_data is not None:
                            time_used_percent = (profiler_data[2] / 1.0) * 100
                            with open(Settings.profiler_filename, "a") as f:
                                f.write(f"{timestamp-Profiler.buffer}: Trends writer used {time_used_percent:.2f}% of time\n")
                    Profiler.updates[timestamp] = (count - 1, start, time_used)
            else:
                Profiler._shutdown()
                break

    @staticmethod
    def _shutdown():
        if Profiler.process:
            Profiler.process.terminate()
            Profiler.process.join()
