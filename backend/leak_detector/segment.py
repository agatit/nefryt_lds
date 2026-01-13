import logging
from math import ceil
from leak_detector.trend import Trend

logger = logging.getLogger(__name__)


class Segment:
    def __init__(self, start: Trend, end: Trend, begin_pos: int, length: float, dist_to_start_node: float,
                 dist_to_end_node: float, wave_speed: float, calc_window: tuple = (True, True)):
        self._length = length
        self._start = start
        self._end = end
        self._begin_pos = begin_pos
        self._end_pos = self._begin_pos + self._length
        self._wave_speed = wave_speed
        self._max_window_size_begin = ceil((dist_to_start_node + self._length) / self._wave_speed) * 1000 if calc_window[0] else 0
        self._max_window_size_end = ceil((dist_to_end_node + self._length) / self._wave_speed) * 1000 if calc_window[1] else 0
        self.no_detection_time = 0
        self._dist_to_start = dist_to_start_node
        self._dist_to_end = dist_to_end_node
        self._flow_time_between_nodes = ((self._dist_to_start + self._dist_to_end + self._length) / self._wave_speed) * 1000

        logger.debug(f"Segment: Created linking between trend with id = {start.id} with trend with id = {end.id}, "
                     f"segment begin position = {self._begin_pos} and length = {self._length}")

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

    @property
    def dist_to_start(self) -> float:
        return self._dist_to_start

    @property
    def dist_to_end(self) -> float:
        return self._dist_to_end

    @property
    def flow_time(self) -> float:
        return self._flow_time_between_nodes
