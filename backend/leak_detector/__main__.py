import logging
from config import setup_engine
from .plant import Plant
from datetime import datetime

# TO DO:
# - Metoda find_leaks_to().
# - Zapisywanie event'ów.
# - Obsługa błędów parametrów i ustalenie domyślnych wartości.
# - Zmienna prędkość rozchodzenia się fali na segmencie.

# Na pewno nie da sie wyznaczyć idelanie miejsca i czasu wycieku bo prędkość fali jest szacowana.
if __name__ == '__main__':
    setup_engine()
    detection_time = 60 * 1000  # ms
    time_between_detections = 1 * 60 * 1000  # ms
    plant = Plant()
    try:
        logging.info('Leak detector started...')
        
        begin_detection_date = datetime(2022, 10, 5, 10, 24)
        begin_detection_time = int(begin_detection_date.timestamp() * 1000)

        while begin_detection_time < datetime(2022, 10, 5, 11, 30).timestamp() * 1000:
            for pipeline in plant.pipelines.values():
                end_detection_time = begin_detection_time + detection_time
                logging.info(f'Detecting leaks from {datetime.fromtimestamp(begin_detection_time / 1000)} '
                             f'to {datetime.fromtimestamp(end_detection_time / 1000)}.')

                leaks = pipeline.find_leaks_in_range(begin_detection_time, end_detection_time)
                print(leaks)
                for method, leak_events in leaks.items():
                    leak_events = sorted(leak_events, key=lambda leak_event: leak_event.datetime)
                    for event in leak_events:
                        logging.info(f'Detected a leak: ({method}) {event.datetime} {pipeline.begin_pos + event.position}m')

            begin_detection_time += time_between_detections

    except Exception as error:
        logging.error(error, exc_info=True)