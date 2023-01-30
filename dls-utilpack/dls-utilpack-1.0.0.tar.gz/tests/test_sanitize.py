import logging

from dls_utilpack.sanitize import sanitize

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestSanitize(BaseTester):
    def test(self, constants, logging_setup, output_directory):
        """ """

        self.main(constants, output_directory)

    # ----------------------------------------------------------------------------------------
    async def _main_coroutine(
        self,
        constants,
        output_directory,
    ):
        """ """

        assert "a-b-c" == sanitize("A/b c--  ")
        assert "a-o-u" == sanitize("ä, ö, ü")
