import atexit
import copy
import logging
import math
import multiprocessing
from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session
from config import setup_engine
from database.models import lds
from db import get_engine
from trends_writer.config import TrendsWriterSettings

logger = logging.getLogger(__name__)


class Profiler:
    queue = None
    process = None
    updates = {}

    @staticmethod
    def init():
        Profiler.queue = multiprocessing.Queue()
        atexit.register(Profiler._shutdown)
        logger.info(f"Profiler: Initialized")

    @staticmethod
    def set_trends(trend_ids: list[str], double_trends_ids: list[str]):
        profiler_dict: dict[str, list] = {'total': [len(trend_ids) + len(double_trends_ids), None]}
        for trend_id in trend_ids:
            profiler_dict[trend_id] = [[1, 0], [None, None, None]]
            if trend_id in double_trends_ids:
                profiler_dict[trend_id] = [[2, 0], [None, None, None]]
        Profiler._start_process(profiler_dict, len(trend_ids))
        logger.info(f"Profiler: Set trends")

    @staticmethod
    def add_profiler_data_to_db(trend_ids: list[str]):
        logger.info(f"Profiler: Started creating profiler data in database")
        for trend_id in trend_ids:
            trend_id = int(trend_id)
            profiler_data = lds.ProfilerData(ID=trend_id)
            with Session(get_engine()) as session:
                try:
                    session.add(profiler_data)
                    session.commit()
                except IntegrityError:
                    session.rollback()
                    old_profiler_data = session.get(lds.ProfilerData, trend_id)
                    session.delete(old_profiler_data)
                    session.add(profiler_data)
                    session.commit()
        logger.info(f"Profiler: Finished creating profiler data in database")

    @staticmethod
    def delete_profiler_data_from_db():
        try:
            with Session(get_engine()) as session:
                session.execute(delete(lds.ProfilerData))
                session.commit()
        except SQLAlchemyError:
            pass

    @staticmethod
    def _start_process(trends_dict: dict, trends_count: int):
        Profiler.process = multiprocessing.Process(target=Profiler._process_queue,
                                                   args=(Profiler.queue, trends_dict, trends_count, TrendsWriterSettings.db_uri,
                                                         TrendsWriterSettings.log_profiler))
        Profiler.process.daemon = True
        Profiler.process.start()
        logger.info("Profiler: Process started")

    @staticmethod
    def _process_queue(queue: multiprocessing.Queue, trends_dict: dict, expected_trends_count: int, db_uri: str,
                       log_profiler: bool):
        setup_engine(db_uri)
        initialized_processes_count = 0
        first_timestamp = math.inf
        while True:
            msg = queue.get()
            operation = msg[0]
            trend_id = msg[1]
            timestamp = msg[2]
            perf_counter = msg[3]
            qsize = msg[4]
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
                    logger.warning(
                        f'Profiler: Already got start time for trend with id={trend_id} (timestamp={timestamp})')
                else:
                    Profiler.updates[timestamp][trend_id][0][0] -= 1
                    Profiler.updates[timestamp][trend_id][0][1] += 1
                    if Profiler.updates[timestamp][trend_id][1][0] is None:
                        Profiler.updates[timestamp][trend_id][1][0] = perf_counter
            elif operation == 0 and timestamp >= first_timestamp:
                if timestamp in Profiler.updates:
                    trends_count, (current_count, finished_count, start, time_used) = Profiler.updates[timestamp][
                        'total']
                    if current_count == 1:
                        time_used += perf_counter - start
                    finished_count += 1
                    current_count -= 1
                    Profiler.updates[timestamp]['total'][1] = (current_count, finished_count, start, time_used)
                    if Profiler.updates[timestamp][trend_id][1][0] is None and Profiler.updates[timestamp][trend_id][1][1] is None:
                        logger.warning(f'Profiler: No start time for trend with id={trend_id} (timestamp={timestamp})')
                    elif Profiler.updates[timestamp][trend_id][1][0] is None and \
                            Profiler.updates[timestamp][trend_id][1][1] is not None:
                        logger.warning(
                            f'Profiler: Already got stop time for trend with id={trend_id} (timestamp={timestamp})')
                    elif Profiler.updates[timestamp][trend_id][0][1] == 1:
                        start_time = Profiler.updates[timestamp][trend_id][1][0]
                        trend_time_used = perf_counter - start_time
                        if Profiler.updates[timestamp][trend_id][1][1] is None:
                            Profiler.updates[timestamp][trend_id][1][1] = trend_time_used
                        else:
                            Profiler.updates[timestamp][trend_id][1][1] += trend_time_used
                        Profiler.updates[timestamp][trend_id][1][2] = qsize
                        Profiler.updates[timestamp][trend_id][1][0] = None
                        Profiler.updates[timestamp][trend_id][0][1] = 0
                        if finished_count >= trends_count and current_count == 0:
                            Profiler.write_profiler_data(log_profiler, time_used, timestamp)
                        else:
                            Profiler.updates[timestamp][trend_id][0][1] -= 0
            elif operation == 2 and timestamp >= first_timestamp:
                if timestamp in Profiler.updates:
                    trends_count, (current_count, finished_count, start, time_used) = Profiler.updates[timestamp]['total']
                    finished_count += trend_id
                    Profiler.updates[timestamp]['total'][1] = (current_count, finished_count, start, time_used)
                    if finished_count >= trends_count and current_count == 0:
                        Profiler.write_profiler_data(log_profiler, time_used, timestamp)
                elif trend_id < trends_dict['total'][0]:
                    Profiler.updates[timestamp] = copy.deepcopy(trends_dict)
                    Profiler.updates[timestamp]['total'][1] = (0, trend_id, None, 0)
            elif operation == 3:
                initialized_processes_count += 1
                if initialized_processes_count == expected_trends_count:
                    first_timestamp = timestamp + 1
            elif operation is None:
                logger.info(f'Profiler: Started shutdown')
                Profiler._shutdown()
                break

    @staticmethod
    def write_profiler_data(log_profiler: bool, time_used: float, timestamp: int):
        time_used_percent = (time_used / 1.0) * 100
        if log_profiler:
            with (open(TrendsWriterSettings.profiler_filename, "a") as f):
                for k, v in Profiler.updates[timestamp].items():
                    if k == 'total' or v[1][1] is None or v[0][0] != 0:
                        continue
                    f.write(f"{timestamp}: Trends writer for trend id={k} used {100 * (v[1][1] / 1.0):.2f}% of time\n")
                    with Session(get_engine()) as session:
                        profiler_data = session.get(lds.ProfilerData, k)
                        if profiler_data:
                            profiler_data.Time10 = float(profiler_data.Time10) * 0.9 + v[1][1] * 0.1 \
                                if profiler_data.Time10 else v[1][1]
                            profiler_data.Time100 = float(profiler_data.Time100) * 0.99 + v[1][1] * 0.01 \
                                if profiler_data.Time100 else v[1][1]
                            profiler_data.Time1000 = float(profiler_data.Time1000) * 0.999 + v[1][1] * 0.001 \
                                if profiler_data.Time1000 else v[1][1]
                            if v[1][2] is not None:
                                profiler_data.QueueSize = v[1][2]
                            session.commit()
                f.write(f"{timestamp}: Trends writer used {time_used_percent:.2f}% of time\n")
        else:
            for k, v in Profiler.updates[timestamp].items():
                if k == 'total' or v[1][1] is None or v[0][0] != 0:
                    continue
                with Session(get_engine()) as session:
                    profiler_data = session.get(lds.ProfilerData, k)
                    if profiler_data:
                        profiler_data.Time10 = float(profiler_data.Time10) * 0.9 + v[1][1] * 0.1 \
                            if profiler_data.Time10 else v[1][1]
                        profiler_data.Time100 = float(profiler_data.Time100) * 0.99 + v[1][1] * 0.01 \
                            if profiler_data.Time100 else v[1][1]
                        profiler_data.Time1000 = float(profiler_data.Time1000) * 0.999 + v[1][1] * 0.001 \
                            if profiler_data.Time1000 else v[1][1]
                        if v[1][2] is not None:
                            profiler_data.QueueSize = v[1][2]
                        session.commit()
        Profiler.updates.pop(timestamp)

    @staticmethod
    def _shutdown():
        Profiler.delete_profiler_data_from_db()
        if Profiler.process:
            Profiler.process.terminate()
            Profiler.process.join()
