import atexit
import copy
import logging
import multiprocessing
from trends_writer.config import Settings


class Profiler:
    queue = None
    process = None
    updates = {}
    max_process_time_buffer = 100

    @staticmethod
    def init():
        Profiler.queue = multiprocessing.Queue()
        atexit.register(Profiler._shutdown)

    @staticmethod
    def set_trends(trend_ids: list[str], double_trends_ids: list[str]):
        profiler_dict = {'total': None}
        for trend_id in trend_ids:
            profiler_dict[trend_id] = None
        Profiler._start_process(profiler_dict, len(trend_ids) + len(double_trends_ids))

    @staticmethod
    def _start_process(trends_dict: dict, trends_count: int):
        Profiler.process = multiprocessing.Process(target=Profiler._process_queue,
                                                   args=(Profiler.queue, trends_dict, trends_count))
        Profiler.process.daemon = True
        Profiler.process.start()

    #TODO: sprawdzic zamykanie timestampa profilera
    @staticmethod
    def _process_queue(queue: multiprocessing.Queue, trends_dict: dict, trends_count: int):
        while True:
            msg = queue.get()
            if msg[0] == 1:
                trend_id = msg[1]
                timestamp = msg[2]
                perf_counter = msg[3]
                if timestamp not in Profiler.updates:
                    Profiler.updates[timestamp] = copy.deepcopy(trends_dict)
                    Profiler.updates[timestamp]['total'] = (1, 0, perf_counter, 0)
                else:
                    current_count, finished_count, start, time_used = Profiler.updates[timestamp]['total']
                    if current_count > 0:
                        Profiler.updates[timestamp]['total'] = (current_count + 1, finished_count, start, time_used)
                    else:
                        Profiler.updates[timestamp]['total'] = (1, finished_count, perf_counter, time_used)
                if Profiler.updates[timestamp][trend_id] is not None:
                    logging.warning(f'Profiler already got start time for {trend_id} in timestamp {timestamp}')
                else:
                    Profiler.updates[timestamp][trend_id] = perf_counter
            elif msg[0] == 0:
                trend_id = msg[1]
                timestamp = msg[2]
                perf_counter = msg[3]
                if timestamp in Profiler.updates:
                    current_count, finished_count, start, time_used = Profiler.updates[timestamp]['total']
                    if current_count == 1:
                        time_used  += perf_counter - start
                    finished_count += 1
                    current_count -= 1
                    Profiler.updates[timestamp]['total'] = (current_count, finished_count, start, time_used)
                    if Profiler.updates[timestamp][trend_id] is None:
                        logging.warning(f'Profiler did not get start time for {trend_id} in timestamp {timestamp}')
                    elif Profiler.updates[timestamp][trend_id] < Profiler.max_process_time_buffer:
                        logging.warning(f'Profiler already got stop time for {trend_id} in timestamp {timestamp}, its {Profiler.updates[timestamp][trend_id]}')
                    else:
                        start_time = Profiler.updates[timestamp][trend_id]
                        trend_time_used = perf_counter - start_time
                        Profiler.updates[timestamp][trend_id] = trend_time_used
                        time_used_percent = (trend_time_used / 1.0) * 100
                        if Settings.log_profiler:
                            with open(Settings.profiler_filename, "a") as f:
                                f.write(f"{timestamp}: Trends writer for trend {trend_id} used {time_used_percent:.2f}% of time\n")
                        if finished_count == trends_count and current_count == 0:
                            time_used_percent = (time_used / 1.0) * 100
                            if Settings.log_profiler:
                                with open(Settings.profiler_filename, "a") as f:
                                    f.write(f"{timestamp}: Trends writer used {time_used_percent:.2f}% of time\n")
                        if finished_count >= trends_count and current_count == 0:
                            Profiler.updates.pop(timestamp)
            elif msg[0] == 2:
                not_started_trends_count = msg[1]
                timestamp = msg[2]
                if timestamp in Profiler.updates:
                    current_count, finished_count, start, time_used = Profiler.updates[timestamp]['total']
                    finished_count += not_started_trends_count
                    Profiler.updates[timestamp]['total'] = (current_count, finished_count, start, time_used)
                    if finished_count >= trends_count and current_count == 0:
                        time_used_percent = (time_used / 1.0) * 100
                        if Settings.log_profiler:
                            with open(Settings.profiler_filename, "a") as f:
                                f.write(f"{timestamp}: Trends writer used {time_used_percent:.2f}% of time\n")
                elif not_started_trends_count < trends_count:
                    Profiler.updates[timestamp] = copy.deepcopy(trends_dict)
                    Profiler.updates[timestamp]['total'] = (0, not_started_trends_count, None, 0)
            else:
                Profiler._shutdown()
                break

    @staticmethod
    def _shutdown():
        if Profiler.process:
            Profiler.process.terminate()
            Profiler.process.join()
