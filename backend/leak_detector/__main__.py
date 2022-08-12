import time
from .plant import Plant

# test

time_offset = 30000 #milisekundy

plant = Plant()

# Wszystkie funkcje, które dostają parametr,
# oznaczający timestamp dostają wartość w milisekundach.

for i in range(10):
    for pipeline in plant.pipelines.values():
        begin_time = (int(time.time()) - 10) * 1000
        current_time = time.time()
        print("START: ", current_time)
        probs = pipeline.find_leaks_in_range(begin_time - time_offset, begin_time)
        print("END:", time.time())
        print("TIME:", time.time() - current_time)
    time.sleep(5)