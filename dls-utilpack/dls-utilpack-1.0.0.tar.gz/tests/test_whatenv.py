import logging

# Version to add to whatenv log.
from dls_utilpack.version import meta as version_meta

# The whatenv class.
from dls_utilpack.whatenv import Whatenv

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestWhatenv:
    def test(self, constants, logging_setup, output_directory):
        """ """

        WhatenvTester().main(constants, output_directory)


# ----------------------------------------------------------------------------------------
class WhatenvTester(BaseTester):
    async def _main_coroutine(self, constants, output_directory):
        """ """

        extra_dict = {"versions": version_meta()}

        # Test whatenv as a direct call with default logger.
        Whatenv(extra_dict=extra_dict).log()
