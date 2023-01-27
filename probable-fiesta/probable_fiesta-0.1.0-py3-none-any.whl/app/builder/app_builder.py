"""App builder module."""
from ...cli.builder.args_parse import Parser
from .context_holder import ContextHolder

class App:
    def __init__(self):
        # properties
        self.name = None
        self.args_parser = None  # validation
        self.arguments = None  # validation
        self.config = None
        self.context = None  # context_holder  # validation
        # internal properties
        self.valid = False
        self.error = None
        self.run_history = []
        self.cleaned_args = []
        self.cleaned_argv = []

    def __str__(self):
        return f"App: {self.__dict__}"

    def validate(self):
        local_valid = True

        # arguments
        if self.arguments is None:
            print("validate fail: App arguments are empty")
            local_valid = False

        # validate args_parser
        if self.args_parser is not None:
            if not self.args_parser.validate(self.arguments):
                print("App args_parser is not valid")
                self.valid = False

        # validate context
        if self.context is not None:
            if not self.context.validate(self.args_parser.get_parsed_args()):
                print("App context is not valid")
                local_valid = False

        self.valid = local_valid
        return self

    def run(self, name=None):
        if not self.valid:
            print("App is not valid.\nTrying to run anyway.")
            #print(self.context)
            command_queue = self.context.command_queue.run_all()
            #print("Command Queue: ", command_queue)
            self.run_history.append(command_queue.get_history())
            return
        #print("App is valid")
        if name is None:
            #print("Running all commands")
            for name in self.context.context_holder.keys():
                #print("Running command for context: ", name)
                context = self.context.context_holder[name]
                #print("context: ", context)
                context_run = context.command_queue.run_all()
                #print("context run: ", context_run)
                context_run_history = context_run.get_history()
                self.run_history.append(context_run_history)
            return
        #print("Running one command for context: ", name)
        command_queue = self.context.context_holder[name].command_queue.run_all()
        #print("Command Queue: ", command_queue)
        self.run_history.append(command_queue.get_history())
        return self

    def get_run_history(self):
        if len(self.run_history) == 0:
            print("No run history found")
            return
        if len(self.run_history) == 1:
            return self.run_history[0]
        return self.run_history

    def clear_run_history(self):
        self.run_history = []
        return self

class AppBuilder:
    
    def __init__(self, app=None): 
        if app is None:
            self.app = App()
        else:
            self.app = app

    @property
    def context(self):
        return AppContextBuilder(self.app)
    
    @property
    def name(self):
        return AppNameBuilder(self.app)

    @property
    def args_parser(self):
        return AppArgsParserBuilder(self.app)

    @property
    def arguments(self):
        return AppArgumentsBuilder(self.app)

    @property
    def config(self):     
        return MyAppConfigBuilder(self.app)

    def build(self):
        return self.app

    def validate(self):
        self.app.validate()
        return self

class AppContextBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def add_context(self, context):
        if self.app.context is None:
            self.app.context = ContextHolder()
        self.app.context.add_context(context)
        return self
    
    def set_context(self, context):
        self.app.context = context
        return self
    
class AppNameBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def set_name(self, name):
        self.app.name = name
        return self

class AppArgsParserBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def add_argument(self, *args, **kwargs):
        if self.app.args_parser is None:
            self.app.args_parser = Parser().Factory.new(add_help=True, description="My app")
        self.app.args_parser.add_argument(*args, **kwargs)
        return self

    def set_args_parser(self, args_parser):
        self.app.args_parser = args_parser
        return self

class AppArgumentsBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def set_arguments(self, arguments):
        self.clean_arguments(arguments)
        self.app.arguments = arguments
        return self

    def clean_arguments(self, arguments):
        #self.app.cleaned_args = []
        #self.app.cleaned_argv = []
        self.app.cleaned_args, self.app.cleaned_argv = self.clean_arg_function(arguments)
        return self

    @staticmethod
    def clean_arg_function(arguments: list):
        args = []
        argv = []
        for x in arguments:  # TODO validate type
            if x.startswith('--'):
                #print("Cleaning x: ", x)
                args.append(x.replace('--', '',2).replace('-', '_'))
            elif x.startswith('-'):
                argv.append(x.replace('-', '',1).replace('-', '_'))
                #print("Cleaning x: ", x)
            else:
                argv.append(x)
                #print("Skipping x: ", x)
        return args, argv


class MyAppConfigBuilder(AppBuilder):
    def __init__(self, app):
        super().__init__(app)

    def set_config(self, config):
        self.app.config = config
        return self