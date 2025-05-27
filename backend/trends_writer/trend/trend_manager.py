class TrendManager:
    _trends = {}

    @staticmethod
    def add(trend):
        TrendManager._trends[trend.id] = trend

    @staticmethod
    def get(trend_id):
        return TrendManager._trends.get(trend_id)

    @staticmethod
    def get_all():
        return TrendManager._trends.values()