from abc import ABC
from enum import Enum, auto
from .my_app_builder import MyAppBuilder
from ...command.builder.command_builder import CommandBuilder
from .context_factory import ContextFactory
from ...config.default_config import get_config
from ...cli.builder.args_parser_factory import ArgsParserFactory

class App(ABC):
    def run(self):
        pass

class MyApp(App):
    def run(self):
        print("This is the my app")

class MetricsApp(App):
    def run(self):
        print("This is the metrics app")

class AppFactory(ABC):
    def create_app(self, name, context, args_parse, args, config):
        pass

    def prepare(self):
        pass
    
    def prepare_default(self):
        pass

class MyappFactory(AppFactory):
    def create_app(self, name, context, args_parse, args, config):
        print("Creating my app")
        my_app_builder = MyAppBuilder()
        my_app = my_app_builder\
            .name\
                .set_name(name)\
            .context\
                .set_context(context)\
            .arguments\
                .validate_with_args_parse(args_parse, args)\
            .config\
                .set_config(config)\
            .build()
        return my_app

    def prepare(self):
        print("Preparing my app")
        return MyApp

    def prepare_default(self):
        print("Preparing default my app sample")
        args = ["--test"]
        function = lambda x: (x)

        # get commands
        command_builder = CommandBuilder()
        commands = command_builder.queue\
            .add_new_command("test", function, args)\
            .build()

        # get context
        context = ContextFactory().new_context("default", commands)
        context.command_queue.print_queue()

        args_parser = ArgsParserFactory().new("--test", action='store_true', help=f"Current version")

        # get config
        config = get_config()

        # create app
        my_app_builder = MyAppBuilder()
        my_app = my_app_builder\
            .name\
                .set_name("sample app")\
            .context\
                .set_context(context)\
            .args_parse\
                .set_args_parse(args_parser)\
            .arguments\
                .set_arguments(args)\
                .validate_args()\
            .config\
                .set_config(config)\
            .build()
        return my_app

class MetricsappFactory(AppFactory):
    def create_app(self, name, context, args_parse, args, config):
        print("Creating metrics app")
        my_app_builder = MyAppBuilder()
        my_app = my_app_builder\
            .name\
                .set_name(name)\
            .context\
                .set_context(context)\
            .args_parse\
                .set_args_parse(args_parse)\
            .arguments\
                .set_arguments(args)\
            .config\
                .set_config(config)\
            .build()
        return my_app

    def prepare(self):
        msg = "Preparing metrics app"
        print(msg)
        return msg

class AppMachine:
    class AvailableApps(Enum):
        MYAPP = auto()
        METRICSAPP = auto()
    
    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            for d in self.AvailableApps:
                name = d.name[0] +  d.name[1:].lower()
                factory_name = name + "Factory"
                factory_instance = eval(factory_name)()
                self.factories.append((name, factory_instance))

    def __str__(self):
        return f"AppMachine: Available apps: {self.factories}"

    def prepare_app(self):
        print("Available apps:")
        for f in self.factories:
            print(f[0])
        s = input(f'Please pick app (0-{len(self.factories)-1}):')
        idx = int(s)
        # specify app name
        return self.factories[idx][1].prepare()

    def prepare_default_app(self):
        return self.factories[0][1].prepare_default()

def prepare_app(type):
    if type == 'my_app':
        return MyappFactory().prepare()
    elif type == 'metrics_app':
        return MetricsappFactory.prepare()
    else:
        print("Invalid app type")
        return None

def prepare_default_app(type):
    if type == 'my_app':
        return MyappFactory().prepare_default()
    else:
        print("Only my_app is supported")
        return None

def flow():
    pass
    # specify app name
    # specify app context
    ## specify app context command_queue
    # specify app args
    # specify app args_parse
    # specify app config