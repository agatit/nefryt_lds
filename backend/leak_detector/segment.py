import logging
from math import ceil
from leak_detector.plant import Pipeline
from leak_detector.trend import Trend


class Segment:
    def __init__(self, pipeline: Pipeline, begin: Trend, end: Trend, begin_pos: int, wave_speed: float):
        distances = pipeline.plant.get_distances(pipeline.plant.nodes[begin.node_id], pipeline.plant.nodes[end.node_id])
        if len(distances) != 1:
            logging.exception(f"There isn't exactly one path between {begin.id} and {end.id}.")
            raise
        self._length = distances[0]
        self._start = begin
        self._end = end
        self._begin_pos = begin_pos
        self._end_pos = self._begin_pos + self._length
        self._wave_speed = wave_speed
        self._max_window_size = ceil(self._length / self._wave_speed) * 1000

        logging.debug(f"Segment {begin.id} <--> {end.id} created.")

    # TODO: Calculate wave speed in one position in pipeline segment
    def calc_wave_speed(self) -> float:
        return self._wave_speed

    @property
    def max_window_size(self) -> int:
        return self._max_window_size

    @property
    def begin_pos(self) -> int:
        return self._begin_pos

    @property
    def length(self) -> float:
        return self._length

    @property
    def start(self) -> Trend:
        return self._start

    @property
    def end(self) -> Trend:
        return self._end
