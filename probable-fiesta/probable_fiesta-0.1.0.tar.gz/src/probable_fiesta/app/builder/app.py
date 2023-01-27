class App:
    def __init__(self):
        self.name = None
        self.args = None
        self.argument_parser = None
        self.validated_args = None
        self.config = None
        self.variables = None
        self.error = None
        self.command = None
        self.command_list = None
        self.command_list_builder = None
        self.command_queue = None

    def __str__(self):
        return f"App: {self.__dict__}"

    def run(self, function):
        """Run command."""
        return function

    def invoke(self):
        if self.command is not None:
            return self.command.invoke()
        else:
            return None

    def run_command_list(self):
        for command in self.command_list:
            command.invoke()
        return self


class MyApp:
    def __init__(self, context=None):
        self.context = context
    
    def __str__(self):
        return f"MyApp: {self.__dict__}"

    @staticmethod
    def new_my_app(context=None):
        return MyApp(context)

    class Factory():
        @staticmethod
        def new_my_app(context=None):
            return MyApp(context)

    factory = Factory()