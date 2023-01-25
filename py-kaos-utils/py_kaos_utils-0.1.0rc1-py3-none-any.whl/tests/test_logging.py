import logging

import pytest
from unittest.mock import patch

from py_kaos_utils.logging import ProgressLogger


@pytest.fixture
def logger():
    return logging.getLogger()


@pytest.mark.parametrize(('checkpoints', 'length'), [(10, 10), (30, 4), (100, 1), (6, 17)])
def test_each_checkpoint_length(logger, checkpoints, length):
    p = ProgressLogger(100, checkpoints=checkpoints, logger=logger)
    assert p._each_checkpoint_length == length


def test_report_progress(logger):
    p = ProgressLogger(100, checkpoints=10, logger=logger)
    p.count_processed += 25
    p.report_progress()
    assert 2 in p._checkpoints_log
    assert p._checkpoints_log[2] == 25


@patch('logging.Logger.info')
def test_log_progress(mock_info, logger):
    p = ProgressLogger(100, checkpoints=10, logger=logger)
    p.log_progress(10)
    mock_info.assert_called_with("10% there: 10/100")
    assert p.count_processed == 10
