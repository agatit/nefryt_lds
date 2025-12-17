import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import setup_engine
from .plant import Plant
from datetime import datetime

# Leaks during tested time periods:
#  - 13:31:00-13:31:03 = XV13 (between PT-01 and PT-02 = trends 101 and 102) = 1205.5m
#  - 13:32:19-13:32:22 = XV16 (between PT-03 and PT-04 = trends 103 and 104) = 183.6m
#  - 13:32:54-13:32:58 = XV12 (between PT-01 and PT-02 = trends 101 and 102) = 1424.7m
#  - 13:33:56-13:34:00 = XV13 (between PT-01 and PT-02 = trends 101 and 102) = 1205.5m
#  - 13:34:35-13:34:36 = XV14 (between PT-02 and PT-03 = trends 102 and 103) = 801.7m
#  - 13:37:12-13:37:15 = XV15 (between PT-02 and PT-03 = trends 102 and 103) = 594.1m
#  - 13:37:48-13:37:53 = XV15 (between PT-02 and PT-03 = trends 102 and 103) = 594.1m
#  - 13:39:23-13:39:25 = XV17 (between PT-03 and PT-04 = trends 103 and 104) = 0.4m
#  - 13:40:15-13:40:18 = XV14 (between PT-02 and PT-03 = trends 102 and 103) = 801.7m
#  - 13:41:19-13:41:24 = XV17 (between PT-03 and PT-04 = trends 103 and 104) = 0.4m
#  - 13:43:55-13:43:59 = XV14 (between PT-02 and PT-03 = trends 102 and 103) = 801.7m
#  - 13:45:15-13:45:20 = XV12 (between PT-01 and PT-02 = trends 101 and 102) = 1424.7m
#  - 13:46:24-13:46:29 = XV12 (between PT-01 and PT-02 = trends 101 and 102) = 1424.7m
#  - 13:47:55-13:47:59 = XV12 (between PT-01 and PT-02 = trends 101 and 102) = 1424.7m
#  - 13:49:10-13:49:11 = XV14 (between PT-02 and PT-03 = trends 102 and 103) = 801.7m
#  - 13:51:03-13:51:05 = XV14 (between PT-02 and PT-03 = trends 102 and 103) = 801.7m
#  - 13:52:33-13:52:34 = XV14 (between PT-02 and PT-03 = trends 102 and 103) = 801.7m
#  - 13:53:55-13:53:58 = XV13 (between PT-01 and PT-02 = trends 101 and 102) = 1205.5m
#  - 13:54:45-13:54:51 = XV12 (between PT-01 and PT-02 = trends 101 and 102) = 1424.7m
#  - 13:55:34-13:55:36 = XV15 (between PT-02 and PT-03 = trends 102 and 103) = 594.1m
#  - 13:58:27-13:58:30 = XV13 (between PT-01 and PT-02 = trends 101 and 102) = 1205.5m
#  - 13:59:17-13:59:19 = XV12 (between PT-01 and PT-02 = trends 101 and 102) = 1424.7m
#  - 14:00:02-14:00:06 = XV13 (between PT-01 and PT-02 = trends 101 and 102) = 1205.5m
#  - 14:00:52-14:00:53 = XV16 (between PT-03 and PT-04 = trends 103 and 104) = 183.6m
#  - 14:01:45-14:01:46 = XV17 (between PT-03 and PT-04 = trends 103 and 104) = 0.4m


if __name__ == '__main__':
    setup_engine()
    plant = Plant()
    detection_time = 10000
    detection_periods = [
        (datetime(2025, 6, 4, 13, 30, 52),
         datetime(2025, 6, 4, 13, 31, 2)),
        (datetime(2025, 6, 4, 13, 39, 20),
         datetime(2025, 6, 4, 13, 39, 30)),
        # (datetime(2025, 6, 4, 13, 30, 52),
        #  datetime(2025, 6, 4, 14, 0, 0)),
    ]

    try:
        logging.info('Leak detector started...')
        for detection_period in detection_periods:
            begin_detection_date = detection_period[0]
            end_detection_date = detection_period[1]
            begin_detection_time = int(begin_detection_date.timestamp() * 1000) - plant.get_leakage_alarm_delta()

            logging.debug(f'Leak detector check time period from {begin_detection_date} to {end_detection_date}')
            while begin_detection_time < detection_period[1].timestamp() * 1000 - plant.get_leakage_alarm_delta():
                end_detection_time = begin_detection_time + plant.get_leakage_alarm_delta() + detection_time
                end_detection_time = end_detection_time if end_detection_time <= (end_detection_date.timestamp() * 1000) else (end_detection_date.timestamp() * 1000)
                for pipeline in plant.pipelines.values():
                    logging.info(f'Detecting leaks from {datetime.fromtimestamp(begin_detection_time / 1000)} '
                                 f'to {datetime.fromtimestamp(end_detection_time / 1000)}.')

                    leaks = pipeline.find_leaks_in_range(begin_detection_time, end_detection_time)
                    for method, leak_events in leaks.items():
                        leak_events = sorted(leak_events, key=lambda leak_event: leak_event.datetime)
                        for event in leak_events:
                            logging.info(f'Leakage detected by method with id = {event.method_id} '
                                         f'in position = {round(pipeline.begin_pos + event.position, 2)}m, date = '
                                         f'{event.datetime}')

                begin_detection_time += detection_time
    except Exception as error:
        logging.error(error, exc_info=True)
