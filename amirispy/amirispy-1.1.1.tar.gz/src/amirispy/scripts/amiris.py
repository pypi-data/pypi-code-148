#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2022 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import logging as log

from amirispy.scripts.subcommands.compare import compare_results
from amirispy.scripts.subcommands.run import run_amiris
from amirispy.scripts.subcommands.install import install_amiris
from amirispy.source.cli import arg_handling_run, Command, CompareOptions, InstallOptions, RunOptions, GeneralOptions
from amirispy.source.logs import set_up_logger, log_and_print


def amiris_cli() -> None:
    """Calls sub-commands with appropriate arguments as returned by the command line parser"""

    command, options = arg_handling_run()
    set_up_logger(options[GeneralOptions.LOG], options[GeneralOptions.LOGFILE])
    if command is Command.INSTALL:
        log.info("Starting install script")
        install_amiris(options[InstallOptions.URL], options[InstallOptions.TARGET])
        log_and_print(f"Successfully installed AMIRIS to {options[InstallOptions.TARGET]}")
    elif command is Command.RUN:
        log.info("Start running AMIRIS")
        run_amiris(options)
        log_and_print(f"Successfully executed AMIRIS. See your results in {options[RunOptions.OUTPUT]}")
    elif command is Command.COMPARE:
        log.info("Starting comparison script")
        compare_results(options[CompareOptions.EXPECTED], options[CompareOptions.TEST], options[CompareOptions.IGNORE])


if __name__ == "__main__":
    amiris_cli()
