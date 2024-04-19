import logging

from .plant import Plant
from datetime import datetime

# Wykresy do sprawdzania wycieku:
# from .tests.plots import global_plot 

# test

detection_time = 60 * 1000 #ms
time_between_detections = 3 * 60 * 1000 #ms
time_delay = 10 * 1000 #ms
plant = Plant()

# Wszystkie funkcje, które dostają parametr,
# który reprezentuje przedział czasu, dostają wartość w milisekundach.

# TO DO:
# - Metoda find_leaks_to().
# - Zmienna prędkość rozchodzenia się fali na segmencie.
 
# Kolejne odległości na zygmuntowie:
# 1. ok. 1428.06m
# 2. ok. 1208.81m
# 3. ok. 805.01m
# 4. ok. 597.51m
# 5. ok. 186.91m
# 6. ok. 3.71m
# Wycieki są w pliku tests/log.txt


detection_time = 60 * 1000 #ms
time_between_detections = 13 * 60 * 1000 #ms
time_delay = 10 * 1000 #ms
plant = Plant()

begin_leaks_date = datetime(2022, 10, 5, 10, 24, 30)
end_leaks_date = datetime(2022, 10, 5, 11, 32, 30)

if __name__ == '__main__':
    try:
        logging.info('Leak detector started...')
        
        begin_detection_time = int(begin_leaks_date.timestamp() * 1000)

        while (begin_detection_time < end_leaks_date.timestamp() * 1000):
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

            # global_plot.show()
    except Exception as error:    
        logging.error(error, exc_info=True)