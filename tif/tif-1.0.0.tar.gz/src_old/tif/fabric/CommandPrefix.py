import string

class CommandPrefix:
    def __init__(self, command, prefix) -> None:
        self.command = command
        self.prefix = prefix

    
    def prefix_command(self) -> string:
        if (self.prefix == ""):
            return "{}".format(self.command)
        return "{}'{}'".format(self.prefix, self.command)