# A small module to implement command validation
from prompt_toolkit.validation import Validator, ValidationError


class CommandValidator(Validator):
    def __init__(self, listOfCommands):
        """
        Constructor for the CommandValidator class.

        :param listOfCommands: A list of strings,
          each of which is a valid command.
        :return self
        """
        self.listOfCommands = set(listOfCommands)

    # An error message we will display if the user tries to
    # run a command that doesn't exist
    def __invalidCommandError(self, commandName):
        return (
            f"'{commandName}' is not a valid command.\n"
            + "Please try agian, or type 'help' for assistance. "
        )

    def validate(self, document):
        # If string is empty, raise
        # a validation error
        if document.text.strip() == "":
            raise ValidationError(message=self.__invalidCommandError(""))

        # Otherwise, get the command name
        commandName = document.text.split(" ")[0]

        # If the command name is not in our list of valid commands,
        # raise a validation error
        if commandName not in self.listOfCommands:
            raise ValidationError(message=self.__invalidCommandError(commandName))
