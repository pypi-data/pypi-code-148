"""Runs Python App. Supports sync and async."""
from datetime import datetime
from ..app import main as main_app
from ..logger.logging_config import get_logger
from ..__about__ import __package_name__
import sys

LOG = get_logger()  # Get logger if needed. Default: INFO

class TimeConfig():

    def __init__(self):
        # record current timestamp
        self.start_time = datetime.now()
        self.end_time = datetime.now()

    def _end(self):
        self.end_time = datetime.now()

    def total_seconds(self):
        self._end()
        td = (self.end_time - self.start_time).total_seconds() * 10**3
        return td


def main(args=None):
    LOG.info(f'Starting package: {__package_name__}')

    # Track time
    LOG.debug("Started tracking execution time of main module.")
    time_config = TimeConfig()

    # Runs main function on app/main.py
    main_app.main(args)

    # End tracking time
    td = time_config.total_seconds()
    LOG.debug(f'Finished tracking execution time of main module: {td:.03f}ms')

    LOG.info(f'Finished package: {__package_name__}\nRun time: {td:.03f}ms')


if __name__ == '__main__':
    main(sys.argv[1:])
