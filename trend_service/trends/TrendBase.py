class TrendBase:
    def __init__(self, trend_ID):
        self.trend_ID = trend_ID
        self.children = []
        self.params = []

    def readParamsFromDB(self):
        pass

    def processData(self):
        pass

    def save(self):
        pass
