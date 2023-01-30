import logging
import os
import subprocess

from dls_utilpack.bash_composer import BashComposer

# Base class for the tester.
from tests.base_tester import BaseTester

logger = logging.getLogger(__name__)


# ----------------------------------------------------------------------------------------
class TestBashComposer(BaseTester):
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
        self.__output_directory = output_directory

        # -------------------------------------
        # Test simple print.
        bash_composer = BashComposer()
        bash_composer.add_print("hello")
        returncode, stdout, stderr = self.__execute_bash(bash_composer)
        assert returncode == 0
        assert stdout.strip() == "hello"
        assert stderr == ""

        # -------------------------------------
        # Test failed command.
        bash_composer = BashComposer()
        bash_composer.add_command("my_bogus_command")
        bash_composer.add_print("hello")
        returncode, stdout, stderr = self.__execute_bash(bash_composer)
        assert returncode == 1
        assert "failed with rc 127" in stdout
        assert "command not found" in stderr
        assert "hello" not in stdout

        # -------------------------------------
        # Test shell command.
        bash_composer = BashComposer()
        bash_composer.add_command("pwd")
        returncode, stdout, stderr = self.__execute_bash(bash_composer)
        assert returncode == 0
        assert os.getcwd() in stdout
        assert stderr == ""

        # -------------------------------------
        # Test loading modules command.

        with open(f"{output_directory}/my_modulefile", "w") as stream:
            stream.write("#%Module1.0\n")
            stream.write("setenv  MY_MODULEFILE_ENV1 env1\n")
            stream.write("setenv  MY_MODULEFILE_ENV2 env2\n")

        bash_composer = BashComposer()
        bash_composer.add_load_modules([output_directory], ["my_modulefile"])
        bash_composer.add_print("MY_MODULEFILE_ENV1=$MY_MODULEFILE_ENV1")
        returncode, stdout, stderr = self.__execute_bash(bash_composer)
        if returncode != 0:
            logger.debug(f"stderr:\n{stderr}")
        assert returncode == 0
        assert "my_modulefile" in stdout
        assert "MY_MODULEFILE_ENV1=env1" in stdout
        assert stderr == ""

        # -------------------------------------
        # Test loading modules command wit non-existent module.
        bash_composer = BashComposer()
        bash_composer.add_load_modules([output_directory], ["my_modulefile_NOTFOUND"])
        returncode, stdout, stderr = self.__execute_bash(bash_composer)
        # assert returncode == 0
        assert "my_modulefile_NOTFOUND" in stdout
        assert stderr == ""

    # ----------------------------------------------------------------------------------------
    def __execute_bash(
        self,
        bash_composer,
    ):
        bash_filename = f"{self.__output_directory}/bash_composed.sh"
        bash_composer.write(bash_filename)
        process = subprocess.run([bash_filename], capture_output=True, encoding="utf-8")

        return process.returncode, process.stdout, process.stderr
