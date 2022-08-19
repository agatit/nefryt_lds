import time
from .plant import Plant

# test

time_offset = 60000 #milisekundy

plant = Plant()

# Wszystkie funkcje, które dostają parametr,
# oznaczający timestamp dostają wartość w milisekundach.

for i in range(10):
    for pipeline in plant.pipelines.values():
        begin_time = (int(time.time()) - 10) * 1000
        current_time = time.time()
        leaks = pipeline.find_leaks_in_range(begin_time - time_offset, begin_time)
        calc_time = time.time() - current_time
        print("LEAKS:")
        for method, events in leaks.items():
            print(" METHOD:", method)
            print(" EVENTS:")
            for event in events:
                print("  TIME: ", event._time)
                print("  POSITION: ", event._position, "m")
                print("")
    time.sleep(5)