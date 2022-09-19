from msilib.schema import Error
import time
import logging

from .plant import Plant
from datetime import datetime

# Wykresy do sprawdzania wycieku:
from .tests.plots import global_plot 

# test

detection_time = 60000 #ms
time_between_detections = 5 #s
time_delay = 100000 #ms
plant = Plant()

# Wszystkie funkcje, które dostają parametr,
# który reprezentuje przedział czasu, dostają wartość w milisekundach.

# TO DO:
# - Metoda find_leaks_to().
# - Ustalenie ostatecznej wersji algorytmu.
# - Zapisywanie event'ów.
# - Obsługa błędów parametrów i ustalenie domyślnych wartości.
# - Zmienna prędkość rozchodzenia się fali na segmencie.
# - 
# - W bazie danych zmienić tabele Trend lub TrendParam, bo dane dot. rejestrów się powtarzają.
# - Może jakoś ładnie pozmieniać importy?

if __name__ == '__main__':
    try:
        logging.info('Leak detector started...')
        
        while (True):
            for pipeline in plant.pipelines.values():
                begin_detection_time = int(time.time()) * 1000 - time_delay
                begin_detection_date = datetime.fromtimestamp(begin_detection_time / 1000)

                end_detection_time = begin_detection_time + detection_time
                end_detection_date = datetime.fromtimestamp(end_detection_time / 1000)

                logging.info(f'Detecting leaks from {begin_detection_date} to {end_detection_date}.')
                leaks = pipeline.find_leaks_in_range(begin_detection_time, end_detection_time)

                for method, events in leaks.items():
                    leaks[method] = sorted(events, key=lambda event: event.datetime)
                    for event in events:
                        logging.info(f'Detected a leak: ({method}) {event.datetime} {event.position}m')

            time.sleep(time_between_detections)
            global_plot.show()
    except Exception as Error:    
        logging.error(Error, exc_info=True)