import copy
import logging
import numpy as np
from scipy.interpolate import interp1d
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import Session
from database import lds
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db import get_engine
from ..plant import Event, Pipeline
from ..segment import Segment
from ..trend import Trend

logger = logging.getLogger(__name__)

class MethodBase:
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        self._pipeline = pipeline
        self._id = id_
        self._name = name

        self._params = {}
        self._read_params()

        logger.info(f"{self.__class__.__name__} ({self.id}): Method initialized (params={self._params})")

    def _read_params(self):
        statement = (select(lds.MethodParam)
                     .select_from(lds.Method)
                     .join(lds.MethodDef, lds.Method.MethodDefID == lds.MethodDef.ID)  # noqa
                     .join(lds.MethodParamDef, lds.MethodDef.ID == lds.MethodParamDef.MethodDefID)
                     .join(lds.MethodParam, and_(lds.MethodParamDef.ID == lds.MethodParam.MethodParamDefID,
                                                 lds.Method.ID == lds.MethodParam.MethodID))
                     .where(lds.Method.ID == self._id))

        with Session(get_engine()) as session:
            method_params = session.scalars(statement).all()
        for mp in method_params:
            self._params[mp.MethodParamDefID.strip()] = mp.Value

    def _get_params(self):
        pass

    def _calculate_params(self):
        pass

    def get_probability(self, segment: Segment, begin: int, end: int) -> list[list[float]]:
        pass

    def find_leaks_in_range(self, begin: int, end: int) -> list[Event]:
        pass

    def find_leaks_to(self, end: int) -> list[Event]:
        pass

    @property
    def pipeline(self) -> Pipeline:
        return self._pipeline

    @property
    def id(self) -> int:
        return self._id

    def get_leakage_alarm_delta(self) -> int:
        return 0

    def get_max_trend_time_delta(self) -> int:
        return 0

    def update_params(self, new_method_params: dict):
        self._params.update(new_method_params)
        self._get_params()
        self._calculate_params()
        logger.debug(f"{self.__class__.__name__} ({self.id}): Method params updated (updated params={new_method_params})")

    def _save_method_data(self, probability: np.ndarray, timestamps: range, positions: range):
        if not self._pipeline.plant.past_leak_detector:
            data_objects = []
            for row, timestamp in enumerate(timestamps):
                for column, position in enumerate(positions):
                    value = probability[row, column]
                    data_object = lds.MethodData(MethodID=self._id, Position=position, Time=timestamp, Value=value)
                    data_objects.append(data_object)

            logger.debug(f"{self.__class__.__name__} ({self.id}): Started saving {len(data_objects)} method data to database")

            with Session(get_engine()) as session:
                session.add_all(data_objects)
                session.commit()

            logger.debug(f"{self.__class__.__name__} ({self.id}): Finished saving {len(data_objects)} method data to database")

    def _delete_method_data_from_db(self):
        if not self._pipeline.plant.past_leak_detector:
            with Session(get_engine()) as session:
                session.execute(delete(lds.MethodData).where(lds.MethodData.MethodID == self.id)) # noqa
                session.commit()

            logger.debug(f"{self.__class__.__name__} ({self.id}): Removed method data from database")


class MethodSegments(MethodBase):
    def __init__(self, pipeline: Pipeline, id_: int, name: str):
        super().__init__(pipeline, id_, name)
        self._stored_events = []
        self._previous_waveform: list[tuple] = [(0, None), (0, None)]

    def _get_params(self):
        try:
            self._pressure_deriv_trend_ids  = str(self._params['PRESSURE_DERIV_TRENDS']).split(',')
            self._segments_like_sensors = bool(self._params.get('SEGMENTS_LIKE_SENSORS', True))
            self._wave_similarity = float(self._params.get('WAVE_SIMILARITY', 1))
            self._wave_speed = float(self._params['BASE_WAVE_SPEED'])
        except KeyError as error:
            raise ValueError(f'{self.__class__.__name__} ({self.id}): No {error.args[0]} param')

        try:
            self._trends : list[Trend] = []
            for trend_id in self._pressure_deriv_trend_ids:
                self._trends.append(self._pipeline.plant.trends[int(trend_id)])
        except KeyError as error:
            raise ValueError(f'{self.__class__.__name__} ({self.id}): Wrong PRESSURE_DERIV_TRENDS value, '
                             f'trend {error.args[0]} does not exist')
        self._begin_pos = self._pipeline.plant.get_distances(self._pipeline.first_node_id, self._trends[0].node_id)[0]

    def _create_segments(self, past_data_needed: bool) -> None:
        logger.debug(f'{self.__class__.__name__} ({self.id}): Started creating segments')
        self._segments: list[Segment] = []
        self._pipeline_length = self._pipeline.begin_pos
        if self._segments_like_sensors:
            previous_trend = None
            for current_trend in self._trends:
                if previous_trend is not None:
                    distances = self.pipeline.plant.get_distances(previous_trend.node_id, current_trend.node_id)
                    if len(distances) != 1:
                        logger.error(f"{self.__class__.__name__} ({self.id}): Not exactly one path between start trend"
                                     f" with node id={previous_trend.node_id} and end trend with node id={current_trend.node_id}")
                    segment_length = distances[0]
                    segment = Segment(previous_trend, current_trend, self._pipeline_length, segment_length,
                                      0, 0, self._wave_speed,
                                      (True, True) if past_data_needed else (False, True))
                    self._pipeline_length += segment.length
                    self._segments.append(segment)
                previous_trend = current_trend
        else:
            for trend_no in range(len(self._trends)-1):
                if trend_no == 0:
                    start_trends = [self._trends[0]]
                    end_trends = [self._trends[1]]
                    distance_parts = [0.75]
                    position_diffs_to_start_node = [(0, (0,1))]
                    position_diffs_to_end_node = [(0.25, (0,1))]
                elif trend_no == len(self._trends)-2:
                    start_trends = [self._trends[-3], self._trends[-2]]
                    end_trends = [self._trends[-1], self._trends[-1]]
                    distance_parts = [0.25, 0.75]
                    position_diffs_to_start_node = [(0.75, (-3,-2)), (0.25, (-2,-1))]
                    position_diffs_to_end_node = [(0.75, (-2,-1)), (0, (-2,-1))]
                else:
                    start_trends = [self._trends[trend_no - 1], self._trends[trend_no]]
                    end_trends = [self._trends[trend_no + 1], self._trends[trend_no + 1]]
                    distance_parts = [0.25, 0.5]
                    position_diffs_to_start_node = [(0.75, (trend_no-1, trend_no)), (0.25, (trend_no, trend_no+1))]
                    position_diffs_to_end_node = [(0.75, (trend_no, trend_no+1)), (0.25, (trend_no, trend_no+1))]
                for start_trend, end_trend, distance_part, (diff_to_start_node, start_node_trends), (diff_to_end_node, end_node_trends) \
                        in zip(start_trends, end_trends, distance_parts, position_diffs_to_start_node, position_diffs_to_end_node):
                    distances = self.pipeline.plant.get_distances(start_trend.node_id, end_trend.node_id)
                    if len(distances) != 1:
                        logger.error(f"{self.__class__.__name__} ({self.id}): Not exactly one path between start trend"
                                     f" with node id={start_trend.node_id} and end trend with node id={end_trend.node_id}")

                    segment_length = distances[0] * distance_part

                    distance_start = self.pipeline.plant.get_distances(self._trends[start_node_trends[0]].node_id, self._trends[start_node_trends[1]].node_id)[0]
                    distance_end = self.pipeline.plant.get_distances(self._trends[end_node_trends[0]].node_id, self._trends[end_node_trends[1]].node_id)[0]
                    segment = Segment(start_trend, end_trend, self._pipeline_length, segment_length,
                                      distance_start * diff_to_start_node, distance_end * diff_to_end_node,
                                      self._wave_speed, (True, True) if past_data_needed else (False, True))
                    self._pipeline_length += segment.length
                    self._segments.append(segment)

        logger.debug(f'{self.__class__.__name__} ({self.id}): Finished creating segments')


    def _find_waves(self, data: np.ndarray, begin: int, start_data: bool) -> np.ndarray:
        data_idx = 0 if start_data is True else 1
        diffs = np.diff(np.sign(data)) != 0
        change_idxs = np.argwhere(diffs)[:, 0]
        if np.sign(data[0]) == 0:
            wave_idxs = [(idx1, idx2) for idx1, idx2 in zip(change_idxs[0::2], change_idxs[1::2]) if
                         (idx2 - idx1) >= 50]
        else:
            wave_idxs = [(idx1, idx2) for idx1, idx2 in zip(change_idxs[1::2], change_idxs[2::2]) if
                         (idx2 - idx1) >= 50]

        result_waveforms = []
        for wave_start_idx, wave_end_idx in wave_idxs:
            if self._previous_waveform[data_idx][1] is None:
                wave_start_timestamp = begin + wave_start_idx * 10
                self._previous_waveform[data_idx] = (wave_start_timestamp, data[wave_start_idx:wave_end_idx])
                result_waveforms.append(data[wave_start_idx:wave_end_idx])
                continue

            previous_wave_timestamp, previous_wave = self._previous_waveform[data_idx]
            wave_start_timestamp = begin + wave_start_idx * 10
            self._previous_waveform[data_idx] = (wave_start_timestamp, copy.deepcopy(data[wave_start_idx:wave_end_idx]))
            current_wave = np.abs(data[wave_start_idx:wave_end_idx])
            previous_wave = np.abs(previous_wave)

            if previous_wave.shape[0] < current_wave.shape[0]:
                interp = interp1d(np.linspace(0, 1, current_wave.shape[0]), current_wave, kind='linear')
                current_wave = interp(np.linspace(0, 1, previous_wave.shape[0]))
            elif current_wave.shape[0] < previous_wave.shape[0]:
                interp = interp1d(np.linspace(0, 1, previous_wave.shape[0]), previous_wave, kind='linear')
                previous_wave = interp(np.linspace(0, 1, current_wave.shape[0]))

            w_current_wave = (current_wave - current_wave.mean()) / (current_wave.std() + 1e-8)
            w_previous_wave = (previous_wave - previous_wave.mean()) / (previous_wave.std() + 1e-8)

            waveforms_corrcoef = np.corrcoef(w_current_wave, w_previous_wave)[0, 1]
            current_max = np.max(current_wave)
            previous_max = np.max(previous_wave)

            if waveforms_corrcoef < self._wave_similarity or current_max > 2 * previous_max:
                result_waveforms.append(data[wave_start_idx:wave_end_idx])
            else:
                result_waveforms.append(np.zeros_like(data[wave_start_idx:wave_end_idx]))

        for waveform, (wave_start_idx, wave_end_idx) in zip(result_waveforms, wave_idxs):
            data[wave_start_idx:wave_end_idx] = waveform

        return data
