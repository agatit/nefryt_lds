import time
from .plant import Plant
from .trend import Trend
import numpy as np

# test

time_offset = 30000 #milisekundy

plant = Plant()

# Wszystkie funkcje, które dostają parametr,
# oznaczający timestamp dostają wartość w milisekundach.

for i in range(10):
    
    for pipeline in plant.pipelines.values():
        if (pipeline.id == 2):
            current_time = (int(time.time()) - 10) * 1000
            probs = pipeline.get_probability(current_time - time_offset, current_time) 
            print("PROBABILITY: ", np.array(probs))
    time.sleep(5)