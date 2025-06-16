import atexit
import copy
import logging
import math
import multiprocessing
from trends_writer.config import Settings


class Profiler:
    queue = None
    process = None
    updates = {}

    @staticmethod
    def init():
        Profiler.queue = multiprocessing.Queue()
        atexit.register(Profiler._shutdown)

    @staticmethod
    def set_trends(trend_ids: list[str], double_trends_ids: list[str]):
        profiler_dict: dict[str, list] = {'total': [len(trend_ids) + len(double_trends_ids), None]}
        for trend_id in trend_ids:
            profiler_dict[trend_id] = [[1, 0], [None, None]]
            if trend_id in double_trends_ids:
                profiler_dict[trend_id] = [[2, 0], [None, None]]
        Profiler._start_process(profiler_dict, len(trend_ids))

    @staticmethod
    def _start_process(trends_dict: dict, trends_count: int):
        Profiler.process = multiprocessing.Process(target=Profiler._process_queue,
                                                   args=(Profiler.queue, trends_dict, trends_count))
        Profiler.process.daemon = True
        Profiler.process.start()

    # TODO: on start => create new OR reset values, then write to db logic, on close => remove
    # TODO: profiler writer tests
    @staticmethod
    def _process_queue(queue: multiprocessing.Queue, trends_dict: dict, expected_trends_count: int):
        initialized_processes_count = 0
        first_timestamp = math.inf
        while True:
            msg = queue.get()
            operation = msg[0]
            trend_id = msg[1]
            timestamp = msg[2]
            perf_counter = msg[3]
            if operation == 1 and timestamp >= first_timestamp:
                if timestamp not in Profiler.updates:
                    Profiler.updates[timestamp] = copy.deepcopy(trends_dict)
                    Profiler.updates[timestamp]['total'][1] = (1, 0, perf_counter, 0)
                else:
                    current_count, finished_count, start, time_used = Profiler.updates[timestamp]['total'][1]
                    if current_count > 0:
                        Profiler.updates[timestamp]['total'][1] = (current_count + 1, finished_count, start, time_used)
                    else:
                        Profiler.updates[timestamp]['total'][1] = (1, finished_count, perf_counter, time_used)
                if Profiler.updates[timestamp][trend_id][0][0] == 0:
                    logging.warning(f'Profiler already got start time for {trend_id} in timestamp {timestamp}')
                else:
                    Profiler.updates[timestamp][trend_id][0][0] -= 1
                    Profiler.updates[timestamp][trend_id][0][1] += 1
                    if Profiler.updates[timestamp][trend_id][1][0] is None:
                        Profiler.updates[timestamp][trend_id][1][0] = perf_counter
            elif operation == 0 and timestamp >= first_timestamp:
                if timestamp in Profiler.updates:
                    trends_count, (current_count, finished_count, start, time_used) = Profiler.updates[timestamp]['total']
                    if current_count == 1:
                        time_used  += perf_counter - start
                    finished_count += 1
                    current_count -= 1
                    Profiler.updates[timestamp]['total'][1] = (current_count, finished_count, start, time_used)
                    if Profiler.updates[timestamp][trend_id][1][0] is None and Profiler.updates[timestamp][trend_id][1][1] is None:
                        logging.warning(f'Profiler did not get start time for {trend_id} in timestamp {timestamp}')
                    elif Profiler.updates[timestamp][trend_id][1][0] is None and Profiler.updates[timestamp][trend_id][1][1] is not None:
                        logging.warning(f'Profiler already got stop time for {trend_id} in timestamp {timestamp}')
                    elif Profiler.updates[timestamp][trend_id][0][1] == 1:
                        start_time = Profiler.updates[timestamp][trend_id][1][0]
                        trend_time_used = perf_counter - start_time
                        if Profiler.updates[timestamp][trend_id][1][1] is None:
                            Profiler.updates[timestamp][trend_id][1][1] = trend_time_used
                        else:
                            Profiler.updates[timestamp][trend_id][1][1] += trend_time_used
                        Profiler.updates[timestamp][trend_id][1][0] = None
                        Profiler.updates[timestamp][trend_id][0][1] = 0
                        if finished_count >= trends_count and current_count == 0:
                            time_used_percent = (time_used / 1.0) * 100
                            if Settings.log_profiler:
                                with open(Settings.profiler_filename, "a") as f:
                                    for k, v in Profiler.updates[timestamp].items():
                                        if k == 'total' or v[1][1] is None:
                                            continue
                                        f.write(f"{timestamp}: Trends writer for trend {k} used {100*(v[1][1] / 1.0):.2f}% of time\n")
                                    f.write(f"{timestamp}: Trends writer used {time_used_percent:.2f}% of time\n")
                            Profiler.updates.pop(timestamp)
                        else:
                            Profiler.updates[timestamp][trend_id][0][1] -= 0
            elif operation == 2 and timestamp >= first_timestamp:
                if timestamp in Profiler.updates:
                    trends_count, (current_count, finished_count, start, time_used) = Profiler.updates[timestamp]['total']
                    finished_count += trend_id
                    Profiler.updates[timestamp]['total'][1] = (current_count, finished_count, start, time_used)
                    if finished_count >= trends_count and current_count == 0:
                        time_used_percent = (time_used / 1.0) * 100
                        if Settings.log_profiler:
                            with open(Settings.profiler_filename, "a") as f:
                                for k, v in Profiler.updates[timestamp].items():
                                    if k == 'total' or v[1][1] is None:
                                        continue
                                    f.write(f"{timestamp}: Trends writer for trend {k} used {100 * (v[1][1] / 1.0):.2f}% of time\n")
                                f.write(f"{timestamp}: Trends writer used {time_used_percent:.2f}% of time\n")
                        Profiler.updates.pop(timestamp)
                elif len(trend_id) < trends_dict['total'][0]:
                    Profiler.updates[timestamp] = copy.deepcopy(trends_dict)
                    Profiler.updates[timestamp]['total'][1] = (0, trend_id, None, 0)
            elif operation == 3:
                initialized_processes_count += 1
                if initialized_processes_count == expected_trends_count:
                    first_timestamp = timestamp + 1
            elif operation is None:
                Profiler._shutdown()
                break

    @staticmethod
    def _shutdown():
        if Profiler.process:
            Profiler.process.terminate()
            Profiler.process.join()
