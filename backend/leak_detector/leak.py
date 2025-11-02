class Leakage:
    def __init__(self, probability: float, position: int, timestamp: int):
        self.probability = probability
        self.timestamp = timestamp
        self.position = position

    def __str__(self):
        return f'Leakage(probability={self.probability}, position={self.position}, timestamp={self.timestamp})'

    def __repr__(self):
        return str(self)
