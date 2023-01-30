import logging

import pytest

from dls_utilpack.substitute import RecursionDepth, substitute_dict, substitute_string

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestSubstitute(BaseTester):
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

        # -----------------------------------------------------------------------------
        # No substitutions leaves the token intact.
        target = "abc ${d.d} efg"
        substitutions = {}
        expected = target
        substituted = substitute_string(target, substitutions)
        assert substituted == target

        dicted = {"field": target}
        substituted = substitute_dict(dicted, substitutions)
        assert dicted["field"] == expected

        # -----------------------------------------------------------------------------
        # Single substitution.
        substitutions = {"d.d": "D"}
        expected = "abc D efg"
        substituted = substitute_string(target, substitutions)
        assert substituted == expected

        dicted = {"field": target}
        substituted = substitute_dict(dicted, substitutions)
        assert dicted["field"] == expected

        # -----------------------------------------------------------------------------
        # One level of recursion in substitution.
        substitutions = {"d.d": "${x.x}", "x.x": "X"}
        expected = "abc X efg"
        substituted = substitute_string(target, substitutions)
        assert substituted == expected

        dicted = {"field": target}
        substituted = substitute_dict(dicted, substitutions)
        assert dicted["field"] == expected

        # -----------------------------------------------------------------------------
        # Three levels of recursion in substitution.
        substitutions = {"d.d": "${x.x}", "x.x": "${y.y}", "y.y": "${z.z}", "z.z": "Z"}
        expected = "abc Z efg"
        substituted = substitute_string(target, substitutions)
        assert substituted == expected

        dicted = {"field": target}
        substituted = substitute_dict(dicted, substitutions)
        assert dicted["field"] == expected

        # -----------------------------------------------------------------------------
        # Too much recursion.
        substitutions = {"d.d": "${x.x}", "x.x": "${d.d}"}

        with pytest.raises(RecursionDepth, match=r".*TEST1.*"):
            substituted = substitute_string(target, substitutions, what="TEST1")

        dicted = {"field": target}

        with pytest.raises(RecursionDepth, match=r".*TEST2.*"):
            substituted = substitute_dict(dicted, substitutions, what="TEST2")
