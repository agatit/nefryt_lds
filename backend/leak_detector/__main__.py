import asyncio
import logging
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import setup_engine
from .plant import Plant
from datetime import datetime, timedelta


logger = logging.getLogger('leak_detector')
detection_time = 30 * 1000


async def leak_detector(plant: Plant):
    max_trend_time_delta_s = plant.max_trend_time_delta
    leakage_alarm_delta_s = plant.max_leakage_alarm_delta // 1000
    logger.info(f'LeakDetector: Module started with params detection time = {detection_time}ms, '
                f'max_trend_time_delta_s = {max_trend_time_delta_s}s, '
                f'leakage_alarm_delta_s = {leakage_alarm_delta_s}s')
    begin_detection_date = datetime.now().replace(microsecond=0)
    end_detection_date = begin_detection_date + timedelta(seconds=detection_time // 1000)
    try:
        while True:
            sleep_time = end_detection_date.timestamp() + leakage_alarm_delta_s + max_trend_time_delta_s + 1 - datetime.now().timestamp()
            time.sleep(sleep_time if sleep_time > 0 else 0)
            logger.info(f'LeakDetector: Detection from {begin_detection_date} to {end_detection_date}')
            begin_detection_time = int(begin_detection_date.timestamp() * 1000) - plant.max_leakage_alarm_delta
            end_detection_time = int(end_detection_date.timestamp() * 1000)
            for pipeline in plant.pipelines.values():
                leaks = pipeline.find_leaks_in_range(begin_detection_time, end_detection_time)
                for method, leak_events in leaks.items():
                    leak_events = sorted(leak_events, key=lambda leak_event: leak_event.datetime)
                    for event in leak_events:
                        event.save()
            begin_detection_date += timedelta(seconds=detection_time//1000)
            end_detection_date += timedelta(seconds=detection_time//1000)
    except KeyboardInterrupt:
        logger.info("LeakDetector: Module shutdown")


if __name__ == '__main__':
    setup_engine()
    asyncio.run(leak_detector(Plant(past_leak_detector=False)))
