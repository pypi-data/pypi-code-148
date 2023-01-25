import logging
import math
from dataclasses import dataclass, field
from logging import Logger

logger = logging.getLogger()


@dataclass
class ProgressLogger:
    """
    Logs the progress of a process by reporting the percentage of completion at a set number of checkpoints.

    Example:
        >>> p = ProgressLogger(1000, 10)
        >>> for count_this_round in [100, 99, 78, 99, 100]:
        >>>     p.log_progress(count_this_round)

    :param count_total: Total number of items to process
    :type count_total: int
    :param checkpoints: Number of checkpoints to report progress at (defaults to 10)
    :type checkpoints: int
    :param logger: Logger instance to use for reporting progress (defaults to the built-in logger)
    :type logger: Logger
    """

    count_total: int
    checkpoints: int = 10
    logger: Logger = logger
    count_processed: int = field(default=0, repr=False, init=False)
    _checkpoints_log: dict = field(default_factory=dict, repr=False, init=False)

    @property
    def _each_checkpoint_length(self):
        """
        :return: Number of items per checkpoint
        :rtype: int
        """
        return math.ceil(self.count_total / self.checkpoints)

    def report_progress(self):
        """
        Report the progress of the process based on the current count_processed value
        """
        checkpoint = self.count_processed // self._each_checkpoint_length
        if checkpoint > len(self._checkpoints_log):
            logger.info(f"{checkpoint / self.checkpoints:.0%} there: {self.count_processed}/{self.count_total}")
            self._checkpoints_log[checkpoint] = self.count_processed

    def log_progress(self, count_this_round, report=True):
        """
        Log the progress of the process

        :param count_this_round: Number of items processed this round
        :type count_this_round: int
        :param report: Whether or not to report the progress (defaults to True)
        :type report: bool
        """
        self.count_processed += count_this_round
        if report:
            self.report_progress()


__all__ = (
    'ProgressLogger',
)
