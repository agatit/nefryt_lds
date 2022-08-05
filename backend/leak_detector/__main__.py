import time
from .plant import Plant
from .trend import Trend
import numpy as np

# test

time_offset = 30 #sekundy
time_resolution = 5  # sekundy
length_resolution = 100 # metry

plant = Plant()

#Trudno jest sprawdzić czy nastąpił wyciek, bo pochodna jest zawsze dodatnia
for i in range(10):
    print(time.time())
    for pipeline in plant.pipelines.values():
        if (pipeline.id == 2):
            current_time = int(time.time())
            probs = pipeline.get_probability(current_time - time_offset, current_time, time_resolution) 
            print("PROBABILITY ON:", np.array(probs))
    time.sleep(5)