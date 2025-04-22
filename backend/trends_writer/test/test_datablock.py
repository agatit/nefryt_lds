from unittest.mock import Mock
import sys
import os
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # noqa: E402
from trends_writer.modbus import PipePlantDataBlock


def test_datablock_calls_pipeplant_update_method_correct_amount_of_times():
    mock_plant1 = Mock()
    block = PipePlantDataBlock(0, [0] * 10, pipe_plant=mock_plant1)

    block.setValues(0, [123])
    mock_plant1.update.assert_called_once()

    mock_plant2 = Mock()
    block = PipePlantDataBlock(0, [0] * 10, pipe_plant=mock_plant2)

    n = 23
    for i in range(n):
        block.setValues(0, [123])

    assert mock_plant2.update.call_count == n


def test_datablock_calls_pipeplant_update_method_with_correct_arguments():
    mock_plant = Mock()
    block = PipePlantDataBlock(0, [0]*10, pipe_plant=mock_plant)
    calls_args = [
        (0, [1, 2]),
        (2, [3, 4])
    ]
    for args in calls_args:
        block.setValues(args[0], args[1])

    for i, call in enumerate(mock_plant.update.call_args_list):
        assert call.args == calls_args[i]


def test_datablock_raises_correct_exceptions():
    mock_plant = Mock()

    with pytest.raises(IndexError):
        PipePlantDataBlock(0, [], pipe_plant=mock_plant)

    mock_plant = Mock()
    mock_plant.update.side_effect = Exception()
    block = PipePlantDataBlock(0, [0]*10, pipe_plant=mock_plant)

    block.setValues(0, [1, 2])


def test_values_are_correctly_updated():
    mock_plant = Mock()
    block = PipePlantDataBlock(0, [0]*10, pipe_plant=mock_plant)

    values = [111, 222]
    block.setValues(0, values)
    assert block.getValues(0, 2) == values
