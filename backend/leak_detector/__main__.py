import time
from .plant import Plant
from .trend import Trend


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

# Pipeline:
#         7
#       /   \ 
# 1 - 2 - 3 - 4 - 5 - 6
#     |
#     8
# Każda rura ma długość 100. 
assert(plant.get_distances(plant.nodes[1], plant.nodes[8], set()) == [200])
assert(plant.get_distances(plant.nodes[1], plant.nodes[6], set()) == [500, 500])
assert(plant.get_distances(plant.nodes[3], plant.nodes[7], set()) == [200, 200])
assert(plant.get_distances(plant.nodes[1], plant.nodes[7], set()) == [400, 200])

# Zbieranie danych z trendów:
timestamp = int(time.time())
data = Trend(1).get_trend_data(timestamp - 10, timestamp)
print(data)
assert(len(data) == 11)
