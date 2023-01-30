import logging

import pytest

from dls_utilpack.datatypes import Datatypes, verify

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# A class providing its own datatypes.
class SomeClass:
    def datatypes(self):
        return "its_own_datatypes"


# ----------------------------------------------------------------------------------------
class TestDatatypes(BaseTester):
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

        assert 1 == verify("x", 1, Datatypes.INTEGER)
        assert 123 == verify("x", "123", Datatypes.INTEGER)

        with pytest.raises(RuntimeError):
            assert 123 == verify("x", "123.4", "wrong datatype")

        with pytest.raises(ValueError):
            assert 123 == verify("x", 123.4, Datatypes.INTEGER)

        with pytest.raises(ValueError):
            assert 123 == verify("x", True, Datatypes.INTEGER)

        with pytest.raises(ValueError):
            assert 123 == verify("x", "123.4", Datatypes.INTEGER)
