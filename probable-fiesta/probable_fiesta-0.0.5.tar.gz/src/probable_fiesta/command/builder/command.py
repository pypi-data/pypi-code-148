"""Command class."""
class Command:

    def __init__(self, name=None, function=None, args=None):
        self.name = name
        self.function = function
        self.args = args

    def __str__(self):
        return f"Command: {self.__dict__}"

    def invoke(self):
        if self.function is not None and self.args is not None:
            return self.function(self.args)
        elif self.function is not None and self.args is None:
            return self.function()
        else:
            print("Missing self.function")
            return None

    @staticmethod
    def new():
        return Command(None, None, None)

    @staticmethod
    def new_with_args(name, function, args):
        return Command(name, function, args)

    class Factory():
        @staticmethod
        def new_command(name, function, args):
            if function is None:
                print("Missing function")
                return None
            return Command(name, function, args)
    
    factory = Factory()
