import os
import stat
from typing import List, Optional


# ---------------------------------------------------------------------
class Element:
    def compose(self) -> List[str]:
        return []


# ---------------------------------------------------------------------
class Prolog(Element):
    def __init__(self):
        pass

    def compose(self) -> List[str]:
        lines = []

        lines.append("#!/bin/bash")
        lines.append("")
        lines.append("# -----------------------------------------------------")
        lines.append("function __execute {")
        lines.append("    echo '$' $1")
        lines.append("    eval $1")
        lines.append("    local rc=$?")
        lines.append("    if [ $rc -ne $2 ]")
        lines.append("    then")
        lines.append("          echo 'command failed with rc' $rc")
        lines.append("          exit 1")
        lines.append("    fi")
        lines.append("}")
        lines.append("# -----------------------------------------------------")

        return lines


# ---------------------------------------------------------------------
class Command(Element):
    def __init__(self, command: str, expected_rc: Optional[int] = 0):
        self.__command = command
        self.__expected_rc = expected_rc

    def compose(self) -> List[str]:
        lines = []

        lines.append("")
        lines.append(f"__execute '{self.__command}' {self.__expected_rc}")

        return lines


# ---------------------------------------------------------------------
class Raw(Element):
    def __init__(self, raw_line):
        self.__raw_line = raw_line

    def compose(self) -> List[str]:
        lines = []

        lines.append(self.__raw_line)

        return lines


# ---------------------------------------------------------------------
class Print(Element):
    def __init__(self, message):
        self.__message = message

    def compose(self) -> List[str]:
        lines = []

        lines.append(f"eval echo '{self.__message}'")

        return lines


# ---------------------------------------------------------------------
class LoadModules(Element):
    def __init__(self, directories: List[str], modules: List[str]):
        """
        Create object which composed to load linux environment modules in the bash script.

        Args:
            directories (List[str]): List of directories for the "module use" command.
            modules (List[str]): List of names for the "module load" command.

        Returns:
            List[str]: Lines to be added to the bash script.
        """
        self.__directories = directories
        self.__modules = modules

    def compose(self) -> List[str]:
        composer = BashComposer(should_include_prolog=False)

        # Establish a USER environment variable.
        composer.add(Raw('export USER="`/usr/bin/id -un`"'))

        # Establish access to linux environment modules.
        MODULESHOME = os.environ.get("MODULESHOME")
        if MODULESHOME is None:
            raise RuntimeError("MODULESHOME environment variable is not set")
        composer.add(Command(f"source {MODULESHOME}/init/bash"))

        # Load the module which supports the ptyrex_recon script.
        composer.add(Command("module purge"))

        for directory in self.__directories:
            composer.add(Command(f"module use --append {directory}"))

        for module in self.__modules:
            composer.add(Command(f"module load {module} 2>&1"))

        # Put a few things in the log.
        composer.add(Command("module list 2>&1"))
        composer.add(Command("python --version"))
        composer.add(Print("------ end of modules_load_bash_lines ------"))

        return composer.compose_lines()


# ---------------------------------------------------------------------
class BashComposer:
    def __init__(self, should_include_prolog: Optional[bool] = True):
        self.__elements: List[Element] = []
        if should_include_prolog:
            self.add(Prolog())

    # -----------------------------------------------------------------
    def add(self, element: Element) -> None:
        self.__elements.append(element)

    # -----------------------------------------------------------------
    def add_print(self, message) -> None:
        self.add(Print(message))

    # -----------------------------------------------------------------
    def add_command(self, command: str, expected_rc: Optional[int] = 0) -> None:
        self.add(Command(command, expected_rc))

    # -----------------------------------------------------------------
    def add_load_modules(self, directories: List[str], modules: List[str]) -> None:
        """
        Add shell commands for loading linux environment modules.

        Args:
            directories (List[str]): List of directories for the "module use" command.
            modules (List[str]): List of names for the "module load" command.
        """
        self.add(LoadModules(directories, modules))

    # -----------------------------------------------------------------
    def compose_lines(self) -> List[str]:
        """
        Return bash script lines.

        Returns:
            List[str]: The complete bash script.
        """

        lines = []
        for element in self.__elements:
            lines.extend(element.compose())

        return lines

    # -----------------------------------------------------------------
    def compose_string(self) -> str:
        """
        Return composed bash script lines.

        Returns:
            str: The complete bash script.
        """

        lines = []
        for element in self.__elements:
            lines.extend(element.compose())

        return "\n".join(lines)

    # -----------------------------------------------------------------
    def write(self, filename: str) -> None:
        """
        Write composed bash script lines to file.

        Adds execution permission to the file.
        """

        with open(filename, "w") as stream:
            stream.write(self.compose_string())
            stream.write("\n")

        st = os.stat(filename)
        os.chmod(filename, st.st_mode | stat.S_IEXEC)
