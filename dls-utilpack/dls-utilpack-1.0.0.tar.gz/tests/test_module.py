import logging
import os

import pytest

from dls_utilpack.module import module_get_environ, module_use

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestModule(BaseTester):
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

        with pytest.raises(RuntimeError) as exception_info:
            module_use("xyz")
        assert "Directory 'xyz' not found" in str(exception_info.value)

        with open(f"{output_directory}/my_modulefile", "w") as stream:
            stream.write("#%Module1.0\n")
            stream.write("setenv  MY_MODULEFILE_ENV1 env1\n")
            stream.write("setenv  MY_MODULEFILE_ENV2 env2\n")
            stream.write(r"setenv  MY_STRING1 {abc}" + "\n")

        os.environ.update(module_use(output_directory))

        with pytest.raises(RuntimeError) as exception_info:
            module_get_environ("xyz")
        expect = "Unable to locate a modulefile for 'xyz'"
        assert expect in str(exception_info.value)

        os.environ.update(module_get_environ("my_modulefile"))

        os.environ.update(module_get_environ("my_modulefile"))

        assert os.environ["MY_MODULEFILE_ENV1"] == "env1"
        assert os.environ["MY_MODULEFILE_ENV2"] == "env2"
