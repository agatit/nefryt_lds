from unittest.mock import Mock, patch
import sys
import os

import numpy as np
import pytest

from trends_writer.trend import TrendDeriv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # noqa: E402
from trends_writer.modbus import PipePlantDataBlock


def test_trend_deriv_calculates_derivative_correctly():
    def mock_read_params(self):
        self.params = {'FILTER_WINDOW': '1.0'}

    def mock_initiate_buffer(self, _, __, ___):
        self.storage = np.arange(0, 300, 3)

    with patch.object(TrendDeriv, '_read_params', new=mock_read_params):
        with patch.object(TrendDeriv, 'start_process_queue', new=lambda _: None):
            with patch.object(TrendDeriv, 'initiate_buffer', new=mock_initiate_buffer):
                mocked_queue = Mock()
                trend = TrendDeriv(1, mocked_queue, None, None)
                a = 3

                for i in range(5):
                    x = np.arange(i*100, (i+1)*100)
                    y = a*x
                    trend.update(y, i+10, None)

                assert 1== 0
