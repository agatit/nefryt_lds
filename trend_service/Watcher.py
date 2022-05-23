from threading import Thread
import threading
import time

class Watcher(Thread):
    def __init__(self, event: threading.Event, callback, time_interval: int = 1, args=(), kwargs={}):
        Thread.__init__(self)
        self.args = args
        self.kwargs = kwargs
        self.stopped = event
        self.time_interval = time_interval
        self.function = callback

    def run(self) -> None:
        while not self.stopped.wait(self.time_interval):
            print("Watcher is running")
            self.function(*self.args, **self.kwargs)
