"""App builder class."""

class MyApp:
    def __init__(self):
        self.context = None  # property
        self.name = None  # property
        self.arguments = None   # property
        self.config = None  # property
        self.args_parse = None  # property required by args

        self.error = None  # required by args_parse
        self.validated_args = None  # required by args_parse
        self.args = None ## remove


    def __str__(self):
        return f"MyApp: {self.context} {self.name} {self.error} {self.validated_args} {self.args_parse} {self.args}"

    def run(self):
        return self.context.command_queue.run_all()

class MyAppBuilder:
    def __init__(self, my_app=None):
        if my_app is None:
            self.my_app = MyApp()
        else:
            self.my_app = my_app
        
    @property
    def context(self):
        return MyAppContextBuilder(self.my_app)
    
    @property
    def name(self):
        return MyAppNameBuilder(self.my_app)

    @property
    def arguments(self):
        return MyAppArgsBuilder(self.my_app)

    @property
    def config(self):     
        return MyAppConfigBuilder(self.my_app)

    @property
    def args_parse(self):
        return MyAppArgsParseBuilder(self.my_app)

    def build(self):
        return self.my_app

    def run(self):
        return self.my_app.run()

class MyAppArgsParseBuilder(MyAppBuilder):
    def __init__(self, my_app):
        super().__init__(my_app)

    def set_args_parse(self, args_parse):
        self.my_app.args_parse = args_parse
        return self

class MyAppContextBuilder(MyAppBuilder):
    def __init__(self, my_app):
        super().__init__(my_app)

    def set_context(self, context):
        self.my_app.context = context
        return self

    def set_context_name(self, name):
        self.my_app.context.name = name
        return self

    def set_context_queue(self, command_queue):
        self.my_app.context.command_queue = command_queue
        return self

class MyAppNameBuilder(MyAppBuilder):
    def __init__(self, my_app):
        super().__init__(my_app)

    def set_name(self, name):
        self.my_app.name = name
        return self

class MyAppArgsBuilder(MyAppBuilder):
    def __init__(self, my_app):
        super().__init__(my_app)

    def set_arguments(self, arguments):
        self.my_app.arguments = arguments
        return self

    def set_args_parse(self, parser):
        self.my_app.args_parse = parser
        return self

    def validate_args(self, args=None):
        if args is not None:
            self.my_app.arguments = args

        a = self.my_app.arguments
        va = None

        if a:
            if self.my_app.args_parse is None:
                raise Exception("No argument parser set.")
            # Validate arguments with args parse
            va = self.my_app.args_parse.parse_args(a)
        else:
            va = self.my_app.args_parse.parse_args(None)

        if self.my_app.args_parse.error_message:
            self.my_app.error = f"{self.my_app.args_parse.error_message}"
        if not va:
            self.my_app.validated_args = None
        else:
            self.my_app.validated_args = va

        return self

    def validate_with_args_parse(self, args_parse, args=None):
        self.set_args_parse(args_parse)
        self.validate_args(args)
        return self
    
    def get_valid_args(self):
        return self.my_app.validated_args

class MyAppConfigBuilder(MyAppBuilder):
    def __init__(self, my_app):
        super().__init__(my_app)

    def set_config(self, config):
        self.my_app.config = config
        return self
