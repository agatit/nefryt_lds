import logging

from .plant import Plant
from datetime import datetime

# Wykresy do sprawdzania wycieku:
from .tests.plots import global_plot 

# test

detection_time = 60 * 1000 #ms
time_between_detections = 3 * 60 * 1000 #ms
time_delay = 10 * 1000 #ms
plant = Plant()

# Wszystkie funkcje, które dostają parametr,
# który reprezentuje przedział czasu, dostają wartość w milisekundach.

# TO DO:
# - Metoda find_leaks_to().
# - Zapisywanie event'ów.
# - Obsługa błędów parametrów i ustalenie domyślnych wartości.
# - Zmienna prędkość rozchodzenia się fali na segmencie.
 

# Zasymulowano wycieki, odległość od początku rurociągu:
# 1. ok. 12:57:40, 1428.06m
# 2. ok. 13:00:40, 1208.81m
# 3. ok. 13:03:40, 805.01m
# 4. ok. 13:06:40, 597.51m
# 5. ok. 13:09:40, 186.91m
# 6. ok. 13:12:40, 3.71m
# Wycieki są od największego od najmniejszego.

# Na pewno nie da sie wyznaczyć idelanie miejsca i czasu wycieku bo prędkość fali
# jest szacowany.
if __name__ == '__main__':
    try:
        logging.info('Leak detector started...')
        
        begin_detection_date = datetime(2022, 9, 20, 12, 57, 30)
        begin_detection_time = int(begin_detection_date.timestamp() * 1000)

        while (begin_detection_time < datetime(2022, 9, 20, 13, 15).timestamp() * 1000):
            for pipeline in plant.pipelines.values():
                begin_detection_date = datetime.fromtimestamp(begin_detection_time / 1000)
            
                end_detection_time = begin_detection_time + detection_time
                end_detection_date = datetime.fromtimestamp(end_detection_time / 1000)

                logging.info(f'Detecting leaks from {begin_detection_date} to {end_detection_date}.')
                leaks = pipeline.find_leaks_in_range(begin_detection_time, end_detection_time)

                for method, events in leaks.items():
                    events = sorted(events, key=lambda event: event.datetime)
                    for event in events:
                        logging.info(f'Detected a leak: ({method}) {event.datetime} {pipeline.begin_pos + event.position}m')

            begin_detection_time += time_between_detections

            global_plot.show()
    except Exception as error:    
        logging.error(error, exc_info=True)