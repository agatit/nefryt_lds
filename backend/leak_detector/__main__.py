import time
from .plant import Plant



# test

time_offset = 30
time_resolution = 0.5
length_resolution = 100

plant = Plant()

for i in range(10):
    print(time.time())
    for pipeline in plant.pipelines.values():
        events = pipeline.find_leaks_to(time.time() - time_offset, time_resolution, length_resolution)
        print(events)
    time.sleep(5)
