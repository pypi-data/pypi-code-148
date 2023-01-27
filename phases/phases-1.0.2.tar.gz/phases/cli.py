"""phases
Usage:
  phases [-v] ...
  phases create [-f] [-p <projectfile>] [-o <outputdir>] [-v]
  phases run <phaseName> [-p <projectfile>] [-c <configfile>] [-o <outputdir>] [--set <configvalues> ...] [-v]
  phases gridrun <phaseName> <gridfile> [-r] [--csv <csvLogFile>] [-p <projectfile>] [-c <configfile>] [-o <outputdir>] [--set <configvalues> ...] [-v]
  phases test [<testdir>] [-p <projectfile>] [-c <configfile>] [-o <outputdir>] [-tp <testpattern>] [-v] [-f]
  phases -h | --help
  phases --version
Options:
  -h --help                         Show this screen.
  --version                         Show version.
  -p <projectfile>                  project file [default: project.yaml]
  -o <outputdir>                    output directory [default: .]
  -f                                force to overwrite existing files
  -v                                verbose output
  -c <configfile>                   use userconfig (project.<configfile>.yaml)
  -g <gridfile>                     use a grid file
  -t <testdir>                      test directory [default: tests]
  -tp <testpattern>                 pattern to look for tests [default: test.py]
  --csv <csvLogFile>                path to an csvfile that should be used for logging
  -r                                restart grid search, instead of resuming from last line in csvLogFile
  --set <configvalues>              overwrite single config values
Examples:
  phases --version
  phases run myPhase
Help:
  For help using this tool, please open an issue on the Gitlab repository: https://gitlab.com/tud.ibmt/phases
"""

from inspect import getmembers, isclass
from docopt import docopt
from phases import __version__ as VERSION
import phases.commands
from phases.commands.Base import Base
import pyPhases
from pyPhases import Logger, LogLevel
import sys

# import phases.commands as commands


def main():
    """Main CLI entrypoint."""
    options = docopt(__doc__, version=VERSION)

    if options["-v"]:
        Logger.verboseLevel = LogLevel.DEBUG

    Logger.log("Phases %s with pyPhases %s (Log level: %s)" % (VERSION, pyPhases.__version__, Logger.verboseLevel), "phases")

    # Here we'll try to dynamically match the command the user is trying to run
    # with a pre-defined command class we've already created.
    for (k, v) in options.items():
        if hasattr(phases.commands, k) and v:
            module = getattr(phases.commands, k)
            commands = getmembers(module, isclass)
            commands = list(filter(lambda c: c[0] != "Base" and issubclass(c[1], Base), commands))

            commandName, command = commands.pop()  # get last defined class to skip imports
            Logger.log("Run Command %s" % (commandName), "phases", LogLevel.DEBUG)
            command = command(options)
            command.run()
            sys.exit()
