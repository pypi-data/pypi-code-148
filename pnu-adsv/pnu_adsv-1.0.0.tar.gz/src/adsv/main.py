#!/usr/bin/env python3
""" adsv - Analyze delimiter-separated values files
License: 3-clause BSD (see https://opensource.org/licenses/BSD-3-Clause)
Author: Hubert Tournier
"""

import getopt
import logging
import os
import sys

import libpnu

from .dsv_library import print_dsv_file_analysis, print_dsv_fields

# Version string used by the what(1) and ident(1) commands:
ID = "@(#) $Id: adsv - Analyze delimiter-separated values files v1.0.0 (January 22, 2023) by Hubert Tournier $"

# Default parameters. Can be overcome by environment variables, then command line options
parameters = {
    "Delimiter": "",
    "Encoding": "",
    "Fields": [],
    "Flatten": False,
    "Hide threshold": 0.2,
    "Max lines": -1,
    "Min count": -1,
    "Top lines": 5,
}


####################################################################################################
def _display_help():
    """ Display usage and help """
    #pylint: disable=C0301
    print("usage: adsv [--debug] [--help|-?] [--version]", file=sys.stderr)
    print("       [-d|--delimiter CHAR] [-e|--encoding STRING]", file=sys.stderr)
    print("       [-f|--fields LIST] [-F|--flatten] [-h|--hide INT]", file=sys.stderr)
    print("       [-m|--min INT] [-M|--max INT] [-t|--top INT]", file=sys.stderr)
    print("       [--] filename [...]", file=sys.stderr)
    print("  --------------------  -------------------------------------------------------", file=sys.stderr)
    print("  -d|--delimiter CHAR   Specify delimiter to be CHAR", file=sys.stderr)
    print("  -e|--encoding STRING  Specify charset encoding to be STRING", file=sys.stderr)
    print("                        (because detecting encoding can take a long time!)", file=sys.stderr)
    print("  -f|--fields LIST      Extract LISTed fields values in given order", file=sys.stderr)
    print("                        (ex: 6,2-4,1 with fields numbered from 1)", file=sys.stderr)
    print("  -F|--flatten          Make multi-lines fields single line", file=sys.stderr)
    print("  -h|--hide INT         Hide the display of distinct values above INT %", file=sys.stderr)
    print("  -m|--min INT          Only display distinct values whose count >= INT", file=sys.stderr)
    print("  -M|--max INT          Only display INT lines of distinct values", file=sys.stderr)
    print("  -t|--top INT          Only display the top/bottom INT lines of values", file=sys.stderr)
    print("  --debug               Enable debug mode", file=sys.stderr)
    print("  --help|-?             Print usage and this help message and exit", file=sys.stderr)
    print("  --version             Print version and exit", file=sys.stderr)
    print("  --                    Options processing terminator", file=sys.stderr)
    print(file=sys.stderr)
    #pylint: enable=C0301


####################################################################################################
def _handle_interrupts(signal_number, current_stack_frame):
    """ Prevent SIGINT signals from displaying an ugly stack trace """
    print(" Interrupted!\n", file=sys.stderr)
    sys.exit(0)


####################################################################################################
def _process_environment_variables():
    """ Process environment variables """
    #pylint: disable=C0103, W0602
    global parameters
    #pylint: enable=C0103, W0602

    if "ADSV_DEBUG" in os.environ:
        logging.disable(logging.NOTSET)

    logging.debug("_process_environment_variables(): parameters:")
    logging.debug(parameters)


####################################################################################################
def _process_command_line():
    """ Process command line options """
    #pylint: disable=C0103, W0602
    global parameters
    #pylint: enable=C0103, W0602

    # option letters followed by : expect an argument
    # same for option strings followed by =
    character_options = "d:e:f:Fh:m:M:t:?"
    string_options = [
        "debug",
        "delimiter=",
        "encoding=",
        "fields=",
        "flatten",
        "help",
        "hide=",
        "max=",
        "min=",
        "top=",
        "version",
        ]

    try:
        options, remaining_arguments = getopt.getopt(
            sys.argv[1:], character_options, string_options
        )
    except getopt.GetoptError as error:
        logging.critical("Syntax error: %s", error)
        _display_help()
        sys.exit(1)

    for option, argument in options:

        if option == "--debug":
            logging.disable(logging.NOTSET)

        elif option in ("--help", "-?"):
            _display_help()
            sys.exit(0)

        elif option == "--version":
            print(ID.replace("@(" + "#)" + " $" + "Id" + ": ", "").replace(" $", ""))
            sys.exit(0)

        elif option in ("-d", "--delimiter"):
            if len(argument) > 1:
                logging.critical("-d|--delimiter argument must be a single character")
                sys.exit(1)
            parameters["Delimiter"] = argument

        elif option in ("-e", "--encoding"):
            parameters["Encoding"] = argument

        elif option in ("-f", "--fields"):
            parts = argument.split(",")
            for element in parts:
                if "-" in element:
                    subparts = element.split("-")
                    try:
                        value1 = int(subparts[0])
                        value2 = int(subparts[1])
                    except ValueError:
                        logging.critical("-f|--fields arguments must be integers")
                        sys.exit(1)
                    if value1 >= value2 or value1 < 1 or value2 < 1:
                        logging.critical(
                            "-f|--fields range arguments must be ascending >= 1 integers"
                            )
                        sys.exit(1)
                    for value in range(value1, value2 + 1):
                        parameters["Fields"].append(value)
                else:
                    try:
                        value = int(element)
                    except ValueError:
                        logging.critical("-f|--fields arguments must be integers")
                        sys.exit(1)
                    if value < 1:
                        logging.critical("-f|--fields arguments must be >= 1 integers")
                        sys.exit(1)
                    parameters["Fields"].append(value)

        elif option in ("-F", "--flatten"):
            parameters["Flatten"] = True

        elif option in ("-h", "--hide"):
            try:
                parameters["Display threshold"] = int(argument) / 100
            except ValueError:
                logging.critical("-h|--hide argument is not an integer")
                sys.exit(1)
            if parameters["Hide threshold"] < 0.01 or parameters["Hide threshold"] > 1:
                logging.critical("-h|--hide argument must be between 1 and 100")
                sys.exit(1)

        elif option in ("-m", "--min"):
            try:
                parameters["Min count"] = int(argument)
            except ValueError:
                logging.critical("-m|--min argument is not an integer")
                sys.exit(1)

        elif option in ("-M", "--max"):
            try:
                parameters["Max lines"] = int(argument)
            except ValueError:
                logging.critical("-M|--max argument is not an integer")
                sys.exit(1)
            if parameters["Max lines"] < 1:
                logging.critical("-M|--max argument must be at least 1")
                sys.exit(1)

        elif option in ("-t", "--top"):
            try:
                parameters["Top lines"] = int(argument)
            except ValueError:
                logging.critical("-t|--top argument is not an integer")
                sys.exit(1)
            if parameters["Top lines"] < 1:
                logging.critical("-t|--top argument must be at least 1")
                sys.exit(1)

    logging.debug("_process_command_line(): parameters:")
    logging.debug(parameters)
    logging.debug("_process_command_line(): remaining_arguments:")
    logging.debug(remaining_arguments)

    return remaining_arguments


####################################################################################################
def main():
    """ The program's main entry point """
    program_name = os.path.basename(sys.argv[0])

    libpnu.initialize_debugging(program_name)
    libpnu.handle_interrupt_signals(_handle_interrupts)
    _process_environment_variables()
    arguments = _process_command_line()

    exit_status = 0

    if not arguments:
        _display_help()

    for argument in arguments:
        if parameters["Fields"]:
            exit_status += print_dsv_fields(
                               argument,
                               parameters["Fields"],
                               delimiter=parameters["Delimiter"],
                               encoding=parameters["Encoding"],
                               flatten=parameters["Flatten"],
                               )
        else:
            exit_status += print_dsv_file_analysis(
                               argument,
                               delimiter=parameters["Delimiter"],
                               encoding=parameters["Encoding"],
                               hide_threshold=parameters["Hide threshold"],
                               max_lines=parameters["Max lines"],
                               min_count=parameters["Min count"],
                               top_lines=parameters["Top lines"],
                               )
        print()

    sys.exit(exit_status)


####################################################################################################
if __name__ == "__main__":
    main()
