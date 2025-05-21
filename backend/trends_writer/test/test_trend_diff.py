import random
import struct
from unittest.mock import Mock, patch
import numpy as np
import pytest
from trends_writer.trend import TrendDiff

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


def test_trend_diff_calculates_difference_correctly_for_different_trends():
    trend_id1 = 1
    trend_id2 = 2
    a1 = 3
    a2 = 5

    def mock_read_params(self):
        self.params = {'TREND_A': trend_id1, 'TREND_B': trend_id2}

    with patch.object(TrendDiff, '_read_params', new=mock_read_params):
        with patch.object(TrendDiff, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDiff, '_save', new=mock_save):
                mocked_queue = Mock()
                trend = TrendDiff(0, mocked_queue, None, None)

                for i in range(5):
                    x1 = np.arange(a1*i*100, a1*(i+1)*100, a1)
                    x2 = np.arange(a2*i*100, a2*(i+1)*100, a2)
                    trend.update(x1, i + timestamp_offset, trend_id1)
                    trend.update(x2, i + timestamp_offset, trend_id2)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        expected_data = np.arange(a1*i*100, a1*(i+1)*100, a1) - np.arange(a2*i*100, a2*(i+1)*100, a2)
        assert np.all(saved_data == expected_data)
        assert saved_timestamp == i + timestamp_offset


def test_trend_diff_calculates_difference_correctly_for_the_same_data():
    trend_id1 = 1
    trend_id2 = 2

    def mock_read_params(self):
        self.params = {'TREND_A': trend_id1, 'TREND_B': trend_id2}

    with patch.object(TrendDiff, '_read_params', new=mock_read_params):
        with patch.object(TrendDiff, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDiff, '_save', new=mock_save):
                mocked_queue = Mock()
                trend = TrendDiff(0, mocked_queue, None, None)

                for i in range(5):
                    x = np.full(100, 5)
                    trend.update(x, i + timestamp_offset, trend_id1)
                    trend.update(x, i + timestamp_offset, trend_id2)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        expected_data = np.full(100, 0)
        assert np.all(saved_data == expected_data)
        assert saved_timestamp == i + timestamp_offset


def test_trend_diff_raise_exception_when_the_same_trend():
    trend_id = 1

    def mock_read_params(self):
        self.params = {'TREND_A': trend_id, 'TREND_B': trend_id}

    with patch.object(TrendDiff, '_read_params', new=mock_read_params):
        with patch.object(TrendDiff, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDiff, '_save', new=mock_save):
                mocked_queue = Mock()
                with pytest.raises(BaseException):
                    TrendDiff(0, mocked_queue, None, None)


def test_trend_diff_calculates_difference_when_only_one_trend_sends_data():
    trend_id1 = 1
    trend_id2 = 2

    def mock_read_params(self):
        self.params = {'TREND_A': trend_id1, 'TREND_B': trend_id2}

    with patch.object(TrendDiff, '_read_params', new=mock_read_params):
        with patch.object(TrendDiff, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDiff, '_save', new=mock_save):
                mocked_queue = Mock()
                trend = TrendDiff(0, mocked_queue, None, None)

                for i in range(5):
                    x1 = np.full(100, 50)
                    x2 = np.full(100, 5)
                    trend.update(x1, i + timestamp_offset, trend_id1)
                    if i >= 2:
                        trend.update(x2, i + timestamp_offset, trend_id2)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        expected_data = np.full(100, 45)
        assert np.all(saved_data == expected_data)
        assert saved_timestamp == i + timestamp_offset + 2
