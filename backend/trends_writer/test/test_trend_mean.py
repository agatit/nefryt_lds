import random
import struct
from unittest.mock import Mock, patch
import numpy as np
import pytest
from trends_writer.trend import TrendMean

random.seed(42)
saved_results = []
timestamp_offset = 10


@pytest.fixture(scope="function", autouse=True)
def reset_saved_results(request):
    global saved_results
    saved_results = []


def mock_save(_, data, timestamp):
    data = data.astype(np.uint16)
    data = np.minimum(data, [np.iinfo(np.uint16).max - 1] * len(data))
    packed_data = struct.pack('<100H', *data)

    unpacked_data = struct.unpack('<100h', packed_data)
    saved_results.append((unpacked_data, timestamp))


def test_trend_mean_calculates_mean_correctly_for_constant_trend():
    filter_window_value = 1
    value = 250

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        storage = np.full(100, value)
        self.storage = np.array(storage)

    with patch.object(TrendMean, '_read_params', new=mock_read_params):
        with patch.object(TrendMean, 'initiate_buffer', new=mock_initiate_buffer):
            with patch.object(TrendMean, '_save', new=mock_save):
                mocked_queue = Mock()
                mocked_queue2 = Mock()
                trend = TrendMean(1, mocked_queue, '', mocked_queue2)

                for i in range(5):
                    x = list(np.flip(np.full(100, value)))
                    trend.update(x, i + timestamp_offset, 0, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        values = np.unique(saved_data)
        assert len(values) == 1
        assert values[0] == value
        assert saved_timestamp == i + filter_window_value + timestamp_offset


def test_trend_mean_calculates_mean_correctly_for_almost_constant_trend():
    filter_window_value = 1
    value = 250

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        storage = [value + (-5 + random.randint(0, 11)) for _ in range(100)]
        self.storage = np.flip(storage)

    with patch.object(TrendMean, '_read_params', new=mock_read_params):
        with patch.object(TrendMean, 'initiate_buffer', new=mock_initiate_buffer):
            with patch.object(TrendMean, '_save', new=mock_save):
                mocked_queue = Mock()
                mocked_queue2 = Mock()
                trend = TrendMean(1, mocked_queue, '', mocked_queue2)

                for i in range(5):
                    x = list(np.flip([value + (-10 + random.randint(0, 21)) for _ in range(100)]))
                    trend.update(x, i + timestamp_offset, 0, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        values = np.unique(saved_data)
        assert np.all(np.isin(values, (value - 1, value, value + 1)))
        assert saved_timestamp == i + filter_window_value + timestamp_offset


def test_trend_mean_calculates_mean_correctly_for_changing_monotonic_trend():
    filter_window_value = 1

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        self.storage = np.flip(np.arange(0, 100, 1))

    with patch.object(TrendMean, '_read_params', new=mock_read_params):
        with patch.object(TrendMean, 'initiate_buffer', new=mock_initiate_buffer):
            with patch.object(TrendMean, '_save', new=mock_save):
                mocked_queue = Mock()
                mocked_queue2 = Mock()
                trend = TrendMean(1, mocked_queue, '', mocked_queue2)

                for i in range(7):
                    if i < 4:
                        start = i * 100
                        end = (i + 1) * 100
                        step = 1
                    else:
                        start = (8 - i) * 100 - 1
                        end = (7 - i) * 100 - 1
                        step = -1
                    x = list(np.flip(np.arange(start, end, step)))
                    trend.update(x, i + 10, 0, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        if i <= len(saved_results) // 2:
            assert np.all(np.diff(np.array(saved_data)) <= 0)
        else:
            assert np.all(np.diff(np.array(saved_data)) >= 0)
        assert saved_timestamp == i + filter_window_value + timestamp_offset


def test_trend_mean_calculates_mean_correctly_with_different_filter_window_values():
    filter_window_values = [1, 2, 3]
    global saved_results
    saved_results = {0: [], 1: [], 2: []}

    def mock_save2(self, data, timestamp):
        data = data.astype(np.uint16)
        data = np.minimum(data, [np.iinfo(np.uint16).max - 1] * len(data))
        packed_data = struct.pack('<100H', *data)

        unpacked_data = struct.unpack('<100h', packed_data)
        saved_results[self.id].append((unpacked_data, timestamp))

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_values[self.id]}

    def mock_initiate_buffer(self, _, __, ___):
        storage = np.full(100, 0)
        self.storage = np.flip(storage)

    with patch.object(TrendMean, '_read_params', new=mock_read_params):
        with patch.object(TrendMean, 'initiate_buffer', new=mock_initiate_buffer):
            with patch.object(TrendMean, '_save', new=mock_save2):
                mocked_queue = Mock()
                mocked_queue2 = Mock()
                trend1 = TrendMean(0, mocked_queue, '', mocked_queue2)
                trend2 = TrendMean(1, mocked_queue, '', mocked_queue2)
                trend3 = TrendMean(2, mocked_queue, '', mocked_queue2)

                for i in range(9):
                    x = list(np.flip(np.full(100, 200 * i)))
                    trend1.update(x, i + timestamp_offset, 0, None)
                    trend2.update(x, i + timestamp_offset, 0, None)
                    trend3.update(x, i + timestamp_offset, 0, None)

    for i, ((saved_data1, saved_timestamp1), (saved_data2, saved_timestamp2), (saved_data3, saved_timestamp3)) \
            in enumerate(zip(saved_results[0][2:], saved_results[1][1:], saved_results[2])):
        assert saved_timestamp1 == i + max(filter_window_values) + timestamp_offset
        assert saved_timestamp2 == i + max(filter_window_values) + timestamp_offset
        assert saved_timestamp3 == i + max(filter_window_values) + timestamp_offset
        assert np.all(np.array(saved_data1) - np.array(saved_data2) == 0)
        assert np.all(np.array(saved_data2) - np.array(saved_data3) == 0)
