import pytest

from ..logging import Loggable


def test_loggable_class(logger):
    class C(Loggable):
        pass

    c = C(logger=logger)
    c.logger.info('testing...')
