import logging
from math import ceil
from leak_detector.plant import Pipeline
from leak_detector.trend import Trend

logger = logging.getLogger(__name__)


class Segment:
    def __init__(self, pipeline: Pipeline, begin: Trend, end: Trend, begin_pos: int, wave_speed: float, calc_window: tuple = (True, True)):
        distances = pipeline.plant.get_distances(pipeline.plant.nodes[begin.node_id], pipeline.plant.nodes[end.node_id])
        if len(distances) != 1:
            raise ValueError(f"There isn't exactly one path between {begin.id} and {end.id} in segment")
        self._length = distances[0]
        self._start = begin
        self._end = end
        self._begin_pos = begin_pos
        self._end_pos = self._begin_pos + self._length
        self._wave_speed = wave_speed
        self._max_window_size_begin = ceil(self._length / self._wave_speed) * 1000 if calc_window[0] else 0
        self._max_window_size_end = ceil(self._length / self._wave_speed) * 1000 if calc_window[1] else 0
        self.no_detection_time = 0
        self.flow_time = (self._length / self._wave_speed) * 1000

        logger.debug(f"Segment: Created linking begin trend with id = {begin.id} with end trend with id = {end.id}")

    def calc_wave_speed(self) -> float:
        return self._wave_speed

    @property
    def max_window_size(self) -> tuple[int, int]:
        return self._max_window_size_begin, self._max_window_size_end

    @property
    def begin_pos(self) -> int:
        return self._begin_pos

    @property
    def end_pos(self) -> float:
        return self._end_pos

    @property
    def length(self) -> float:
        return self._length

    @property
    def start(self) -> Trend:
        return self._start

    @property
    def end(self) -> Trend:
        return self._end
