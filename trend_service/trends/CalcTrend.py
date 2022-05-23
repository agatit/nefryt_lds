import logging
from sys import argv

from trend_service.Watcher import Watcher

from ..database import orm
from .TrendBase import TrendBase
import threading
import time
class CalcTrend(TrendBase):

    def __init__(self, trend: orm.Trend):
        super().__init__(trend)
        # self.recent_save_time = time.time()
        # self.time_interval = 1
        # self.repeat_watcher_stop_flag = threading.Event()
        # self.repeat_watcher = Watcher(event=self.repeat_watcher_stop_flag, callback=print, time_interval=self.time_interval, args=(self.recent_save_time,))
        

    def processData(self, data, parent_id: int = None):
        try:
            result = self.calculate(data, parent_id)
            if result is not None:
                self.save(result)
        except Exception as e:
            raise e

    def calculate(self, data, parent_id: int = None):
        raise NotImplementedError
