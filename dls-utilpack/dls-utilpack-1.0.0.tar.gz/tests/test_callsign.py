import logging

from dls_utilpack.callsign import callsign

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# A class providing its own callsign.
class SomeClass:
    def callsign(self):
        return "its_own_callsign"


# ----------------------------------------------------------------------------------------
class TestCallsign(BaseTester):
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

        # Callsign of a type.
        assert callsign(int) == "builtins.int"

        # Callsign of a class.
        assert callsign(TestCallsign) == "tests.test_callsign.TestCallsign"

        # Callsign of an instance.
        assert callsign(self) == "tests.test_callsign.TestCallsign"

        # Callsign of a class.
        assert callsign(SomeClass) == "tests.test_callsign.SomeClass"

        # Callsign of an instance with its own callsign method.
        some_object = SomeClass()
        assert callsign(some_object) == "its_own_callsign"
