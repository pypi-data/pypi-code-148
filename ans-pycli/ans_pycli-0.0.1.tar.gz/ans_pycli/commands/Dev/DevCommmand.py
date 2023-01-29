from ans_pycli.commands import NestedCommand, Command


class TestCommand(Command):
    _name = "test"
    _description = "Prints 'Test command'"
    _help = "Test command"
    @staticmethod
    def _func(): print("Test command")


class DevCommand(NestedCommand):
    _name = "dev"
    _description = "Provide development commands"
    _subparsers = {
        "commands": [
            TestCommand(),
        ]
    }
