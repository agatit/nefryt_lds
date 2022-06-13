import logging

from database import lds
from .TrendBase import TrendBase


class QuickTrend(TrendBase):

    def __init__(self, trend: lds.Trend):
        super().__init__(trend)
        logging.info(self.__class__.__name__ + ": initialized")

    def processData(self, data, parent_id: int = None):
        try:
            for child in self.children:
                # timestamp = int(time.time())
                child.processData(data, parent_id)
        except Exception as e:
            logging.exception(e)
            # raise e
