import logging
import os
import re
import shlex
import subprocess

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------------
def module_get_environ(name):
    """
    Load an environment module.
    Supports modules which set environment variables only.
    This just adds or modifies os.environ.
    """

    # Run the command to ask the module system what it wants to do.
    environ_dict = __modulecmd_bash(f"load {name}")

    return environ_dict


# -----------------------------------------------------------------------------------
def module_use(directory):
    """
    Add directory to search path for modules.
    This just adds or modifies os.environ.
    """

    if not os.path.exists(directory):
        raise RuntimeError(f"Directory '{directory}' not found")

    # Run the command to ask the module system what it wants to do.
    environ_dict = __modulecmd_bash(f"use {directory}")

    return environ_dict


# -----------------------------------------------------------------------------------
def __modulecmd_bash(command):
    """
    Add directory to search path for modules.
    This just adds or modifies os.environ.
    """

    full_command = f"modulecmd bash {command}"

    # Run the command to ask the module system what it wants to do.
    logger.debug(f"full_command: {full_command}")
    result = subprocess.run(full_command, shell=True, capture_output=True)
    stderr = result.stderr.decode().strip()
    stdout = result.stdout.decode().strip()

    # Unfortunately, modulecmd returns code 0 even when it can't find the module.
    # To make it more complex, a lot of modulefiles emit welcome messages to stderr.
    # So in this case, we have to examine the stderr for modulecmd's specific format.
    pattern = re.compile(r".*ERROR:.*")
    match = pattern.match(stderr)

    if result.returncode != 0 or match:
        # The verbose output from modulecmd goes to stderr,
        # so we have to ignore lines starting with blank or tab.
        stderr_lines = []
        for line in stderr.split("\n"):
            if len(line) > 0 and line[0] != " " and line[0] != chr(9):
                stderr_lines.append(line)

        if len(stderr_lines) > 0:
            raise RuntimeError(f"{full_command} error: {stderr_lines[0]}")
        else:
            raise RuntimeError(f"{full_command} return code {result.returncode}")

    # Read the stdout lines the module command responds with.
    # stdout_lines = stdout.split("\n")

    # TODO: Allow module load to parse tcl values with semicolons in them.
    # stdout = stdout.replace("\\;", "++")
    if "\\;" in stdout:
        raise RuntimeError(
            f'found invalid semicolon while parsing output from "{command}"'
        )

    # Sometimes tcl will omit a space after a semicolon,
    # so add one to make sure we get a split.
    stdout = stdout.replace(";", "; ")

    s = shlex.shlex(stdout, punctuation_chars=True)
    s.whitespace_split = True
    shlex_lines = list(s)

    tokens = ["$PATH", "$PYTHONPATH"]
    token_values = {}
    for token in tokens:
        token_value = os.environ.get(token[1:])
        if token_value is not None:
            token_values[token] = token_value

    shlex_splitter = re.compile(r"^([^ ;=]+)[=]([^;]*).*$")
    environ_dict = {}
    for shlex_line in shlex_lines:
        parts = shlex_splitter.split(shlex_line)
        # logger.debug(describe(f"shlex_line {shlex_line} splits into", parts))
        if len(parts) == 4:
            keyword = parts[1]
            # As a special case, replace some environment variables.
            # TODO: Add better handling of bash variables present in module load output.
            value = parts[2]

            # Replace certain tokens in the value.
            for token in tokens:
                if token in token_values:
                    value = value.replace(token, token_values[token])

                # We are updating the token value?
                if keyword == token[1:]:
                    token_values[token] = value

            environ_dict[keyword] = value

    return environ_dict
