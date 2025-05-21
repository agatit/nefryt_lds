import random
import struct
from unittest.mock import Mock, patch
import numpy as np
import pytest

from trends_writer.trend import TrendDeriv


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


def test_trend_deriv_calculates_derivative_correctly_for_constant_increasing_trend():
    filter_window_value = 1
    a = 3

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        self.storage = np.arange(0, 300, a)

    with patch.object(TrendDeriv, '_read_params', new=mock_read_params):
        with patch.object(TrendDeriv, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDeriv, 'initiate_buffer', new=mock_initiate_buffer):
                with patch.object(TrendDeriv, '_save', new=mock_save):
                    mocked_queue = Mock()
                    trend = TrendDeriv(1, mocked_queue, None, None)

                    for i in range(5):
                        x = np.arange(i*100, (i+1)*100, a)
                        trend.update(x, i+timestamp_offset, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        values = np.unique(saved_data)
        assert len(values) == 1
        assert values[0] == a*100
        assert saved_timestamp == i + filter_window_value + timestamp_offset


def test_trend_deriv_calculates_derivative_correctly_for_almost_constant_trend():
    filter_window_value = 2

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        storage = [500 + (-2 + random.randint(0, 5)) for _ in range(100)]
        self.storage = np.array(storage)

    with patch.object(TrendDeriv, '_read_params', new=mock_read_params):
        with patch.object(TrendDeriv, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDeriv, 'initiate_buffer', new=mock_initiate_buffer):
                with patch.object(TrendDeriv, '_save', new=mock_save):
                    mocked_queue = Mock()
                    trend = TrendDeriv(1, mocked_queue, None, None)

                    for i in range(7):
                        x = [500 + (-2 + random.randint(0, 5)) for _ in range(100)]
                        trend.update(x, i+timestamp_offset, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        values = np.unique(saved_data)
        assert len(values) == 1
        assert values[0] == 0
        assert saved_timestamp == i + filter_window_value + timestamp_offset


def test_trend_deriv_calculates_derivative_correctly_for_almost_constant_decreasing_trend():
    filter_window_value = 1
    start_value = 3000
    a = 5

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        storage = [start_value - ii*5 + (-5 + random.randint(0, 11)) for ii in range(100)]
        self.storage = np.array(storage)

    with patch.object(TrendDeriv, '_read_params', new=mock_read_params):
        with patch.object(TrendDeriv, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDeriv, 'initiate_buffer', new=mock_initiate_buffer):
                with patch.object(TrendDeriv, '_save', new=mock_save):
                    mocked_queue = Mock()
                    trend = TrendDeriv(1, mocked_queue, None, None)

                    for i in range(5):
                        x = [start_value - i*100*a - ii*5 + (-5 + random.randint(0, 11)) for ii in range(100)]
                        trend.update(x, i+10, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        values = np.unique(saved_data)
        for value in values:
            assert -a*100 - a <= value <= -a*100 + a
        assert saved_timestamp == i + filter_window_value + timestamp_offset


def test_trend_deriv_calculates_derivative_correctly_for_changing_monotonic_trend():
    filter_window_value = 1

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        self.storage = np.arange(0, 100, 1)

    with patch.object(TrendDeriv, '_read_params', new=mock_read_params):
        with patch.object(TrendDeriv, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDeriv, 'initiate_buffer', new=mock_initiate_buffer):
                with patch.object(TrendDeriv, '_save', new=mock_save):
                    mocked_queue = Mock()
                    trend = TrendDeriv(1, mocked_queue, None, None)

                    for i in range(6):
                        if i < 3:
                            start = i*100
                            end = (i+1)*100
                            step = 1
                        else:
                            start = (6-i)*100-1
                            end = (5-i)*100-1
                            step = -1
                        x = np.arange(start, end, step)
                        trend.update(x, i+10, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        if i < len(saved_results) // 2:
            assert np.all(np.array(saved_data) >= 0)
        else:
            assert np.all(np.array(saved_data) <= 0)
        assert saved_timestamp == i + filter_window_value + timestamp_offset


def test_trend_deriv_calculates_derivative_correctly_for_plateau_trend():
    filter_window_value = 1
    a = 3

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        self.storage = np.arange(0, 100*a, a)

    with patch.object(TrendDeriv, '_read_params', new=mock_read_params):
        with patch.object(TrendDeriv, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDeriv, 'initiate_buffer', new=mock_initiate_buffer):
                with patch.object(TrendDeriv, '_save', new=mock_save):
                    mocked_queue = Mock()
                    trend = TrendDeriv(1, mocked_queue, None, None)

                    for i in range(16):
                        if i % 8 == 0:
                            x = np.arange(0, 100*a, a)
                        elif i % 8 == 4:
                            x = np.arange(99*a, -a, -a)
                        else:
                            value = 0 if i % 8 in (5, 6, 7) else 100*a
                            x = np.full(100, value)
                        trend.update(x, i+10, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        if i in (0, 6, 7, 8):
            np.all(np.array(saved_data) >= 0)
        elif i in (1, 5, 9, 13):
            assert np.all(np.array(saved_data) == 0)
        else:
            assert np.all(np.array(saved_data) <= 0)
        assert saved_timestamp == i + filter_window_value + timestamp_offset


def test_trend_deriv_calculates_derivative_correctly_for_almost_constant_step_trend():
    filter_window_value = 2

    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': filter_window_value}

    def mock_initiate_buffer(self, _, __, ___):
        storage = [(-5 + random.randint(0, 11)) for _ in range(100)]
        self.storage = np.array(storage)

    with patch.object(TrendDeriv, '_read_params', new=mock_read_params):
        with patch.object(TrendDeriv, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDeriv, 'initiate_buffer', new=mock_initiate_buffer):
                with patch.object(TrendDeriv, '_save', new=mock_save):
                    mocked_queue = Mock()
                    trend = TrendDeriv(1, mocked_queue, None, None)

                    for i in range(7):
                        x = [(i + -5 + random.randint(0, 11)) for _ in range(100)]
                        trend.update(x, i+timestamp_offset, None)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        values = np.unique(saved_data)
        assert np.all(np.isin(values, (0, 1)))
        assert saved_timestamp == i + filter_window_value + timestamp_offset

# def test_trend_mean_calculates_mean_correctly():
#     def mock_read_params(self):
#         self.params = {'FILTER_WINDOW': '1.0'}
#
#     def mock_initiate_buffer(self, _, __, ___):
#         self.storage = 100 * np.ones(100)
#
#     with patch.object(TrendMean, '_read_params', new=mock_read_params):
#         with patch.object(TrendMean, 'start_process_queue', new=lambda _: None):
#             with patch.object(TrendMean, 'initiate_buffer', new=mock_initiate_buffer):
#                 mocked_queue = Mock()
#                 trend = TrendMean(1, mocked_queue, None, None)
#                 # a = 3
#
#                 for i in range(5):
#                     # x = np.arange(i*100, (i+1)*100)
#                     # y = a*x
#                     y = 100 * np.ones(100)
#                     trend.update(y, i+10, None)
#                     # print(trend.storage)
#
#                 assert 1== 0
