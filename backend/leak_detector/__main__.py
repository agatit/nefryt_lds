import logging
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import setup_engine
from .plant import Plant
from datetime import datetime

# Leaks during tested time periods:
# - 13:24:45-13:24:49 = XV17 (between PT-03 and PT-04 = trends 103 and 104) = 0,4m
# - 13:25:33-13:25:34 = XV13 (between PT-01 and PT-02 = trends 101 and 102) = 1205,5m
# - 13:26:55-13:26:59 = XV15 (between PT-02 and PT-03 = trends 102 and 103) = 594,1m
# - 13:28:26-13:28:30 = XV17 (between PT-03 and PT-04 = trends 103 and 104) = 0,4m


if __name__ == '__main__':
    setup_engine()
    plant = Plant()
    detection_time = 5000
    datection_periods = [
        (datetime(2025, 6, 4, 13, 24, 40),
         datetime(2025, 6, 4, 13, 25, 10)),
        (datetime(2025, 6, 4, 13, 25, 30),
         datetime(2025, 6, 4, 13, 26, 0)),
        (datetime(2025, 6, 4, 13, 26, 52),
         datetime(2025, 6, 4, 13, 27, 22)),
        (datetime(2025, 6, 4, 13, 28, 25),
         datetime(2025, 6, 4, 13, 28, 55)),
    ]

    try:
        logging.info('Leak detector started...')

        for detection_period in datection_periods:
            begin_detection_date = detection_period[0]
            begin_detection_time = int(begin_detection_date.timestamp() * 1000)

            logging.info(f'Leak detector check time period from {detection_period[0]} to {detection_period[1]}')
            while begin_detection_time < detection_period[1].timestamp() * 1000:
                for pipeline in plant.pipelines.values():
                    end_detection_time = begin_detection_time + detection_time
                    logging.info(f'Detecting leaks from {datetime.fromtimestamp(begin_detection_time / 1000)} '
                                 f'to {datetime.fromtimestamp(end_detection_time / 1000)}.')

                    leaks = pipeline.find_leaks_in_range(begin_detection_time, end_detection_time)
                    for method, leak_events in leaks.items():
                        leak_events = sorted(leak_events, key=lambda leak_event: leak_event.datetime)
                        for event in leak_events:
                            logging.info(f'Detected a leak: ({method}) {event.datetime} {pipeline.begin_pos + event.position}m')

                begin_detection_time += detection_time

    except Exception as error:
        logging.error(error, exc_info=True)