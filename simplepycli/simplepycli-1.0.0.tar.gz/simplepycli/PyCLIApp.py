# Declares our main CLI app class, which has functions
# that can be used as decorators for custom client code.
import subprocess

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import (
    FuzzyWordCompleter,
)

from .CommandValidator import CommandValidator


class PyCLIApp:
    def __init__(self, promptTitle="> "):
        # This dict stores tuples of (commandFunction, helpText),
        # with the key being the command name.
        self.commands = {}

        # The run flag of this CLI app; loop exits when this
        # is False
        self.runFlag = True

        # Manually register some commands
        self.commands["exit"] = (
            self.exit,
            "Exit the current CLI session and close the program.",
        )
        self.commands["help"] = (
            self.help,
            "List available commands and their help messages.",
        )
        self.commands["clear"] = (
            self.clear,
            "Clear the current command line.",
        )

        self.promptTitle = promptTitle

    def command(self, commandName, helpText):
        """
        Function decorator for registering a command with the CLI.
        :param commandName: The name of the command to register.
        :param helpText: The help text to display for the command.

        :return None
        """
        # This is what @command(...) evaluates to, and takes the
        # function we're wrapping around as a paramater.
        # This needs to return a function, which can then be
        # called by client code
        def firstInner(f):
            # Before doing anything else, register the given function
            # with self
            self.commands[commandName] = (f, helpText)

            # This is the function that will be called by client
            # code, and is responsible for calling the wrapped function
            def toCall(*args, **kwargs):
                f(*args, **kwargs)

            return toCall

        return firstInner

    # A default command to exit from the CLI without
    # using sys.exit; allows for nested loops.
    def exit(self, params):
        self.runFlag = False

    # A default command to ask for command help
    def help(self, params):
        for command in self.commands:
            print(f"{command} : {self.commands[command][1]}")

    # A defult command to clear the current command line
    def clear(self, params):
        subprocess.run("clear", shell=True)

    # An error message we will display if the user tries to
    # run a command that doesn't exist
    def __invalidCommandError(self, commandName):
        return (
            f"'{commandName}' is not a valid command.\n"
            + "Please try agian, or type 'help' for assistance. "
        )

    # A helper function to split the user's input text into a command
    # and params
    def __inputToParmsAndText(self, txt):
        """
        Takes a string of text and splits it into a command name and
        a string of parameters.

        :param txt: The string of text to split.

        :return (commandName, params): A tuple of the command name and
        the parameters.
        """
        # If input is empty, return empty
        if txt.strip() == "":
            return ("", "")

        commandName = txt.split()[0]
        params = txt.replace(f"{commandName} ", "")
        return (commandName, params)

    def run(self):
        """
        Starts the CLI session with all custom commands available.
        """

        # Get a word completer for all supported commands
        commandWordCompleter = FuzzyWordCompleter(list(self.commands.keys()))

        # Use the CommandValidator class to validate commands
        commandValidator = CommandValidator(self.commands.keys())

        # Construct our prompt session
        cliPromptSession = PromptSession(
            message=self.promptTitle,
            completer=commandWordCompleter,
            validator=commandValidator,
        )

        # Set our run flag to true; this will be negated by the exit command
        # to stop this run loop. Allows for really simple nested interfaces.
        self.runFlag = True

        while self.runFlag:
            # When we run our prompt, the first word is our command
            # name, and the rest are the params we are going to
            # give to the command function;
            # this prompt goes through a command
            # validator, so we don't need to double
            # check for an invalid command name
            userInput = cliPromptSession.prompt()

            commandName, params = self.__inputToParmsAndText(userInput)

            # Run our command
            self.commands[commandName][0](params)
