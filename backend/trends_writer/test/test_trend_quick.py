import random
import struct
from unittest.mock import Mock, patch
import numpy as np
import pytest
from trends_writer.trend import TrendQuick

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


def test_trend_quick_saves_correct_data():
    def mock_read_params(self):
        self.params = {'MODBUS_REGISTER': 1000}

    with patch.object(TrendQuick, '_read_params', new=mock_read_params):
        with patch.object(TrendQuick, '_save', new=mock_save):
            mocked_queue = Mock()
            mocked_queue2 = Mock()
            trend = TrendQuick(0, mocked_queue, '', mocked_queue2)

            for i in range(5):
                x = np.full(100, i*100)
                trend.update(x, i + timestamp_offset, 0)

    for i, (saved_data, saved_timestamp) in enumerate(saved_results):
        expected_data = np.full(100, i*100)
        assert np.all(saved_data == expected_data)
        assert saved_timestamp == i + timestamp_offset
