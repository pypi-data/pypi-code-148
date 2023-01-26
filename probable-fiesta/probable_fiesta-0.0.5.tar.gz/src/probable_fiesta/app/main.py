""""Main module for probable_fiesta app."""
import sys

from ..config.variables import PackageDef as pd
from ..config.variables import VariablesDef as vd
from ..app.builder.my_app_builder import MyAppBuilder
from ..app.builder.context_factory import ContextFactory
from ..command.builder.command_builder import CommandBuilder
from ..config.default_config import get_config
from ..command.builder.command import Command
from ..app.builder.app_abstract_machine import AppMachine
from ..cli.builder.parser_builder import ParserBuilder


def default_app_builder(name, context, args_parse, args, config):
    my_app_builder = MyAppBuilder()
    # Create main app
    main_app = my_app_builder\
        .name\
            .set_name(name)\
        .context\
            .set_context(context)\
        .args_parse\
            .set_args_parse(args_parse)\
        .arguments\
            .set_arguments(args)\
            .validate_args()\
        .config\
            .set_config(config)\
        .build()
    return main_app

def build_commands():
    command_builder = CommandBuilder()
    commands = command_builder.queue\
        .add_new_command("version", get_version)\
        .add_new_command("repeat", repeat, "--this-is-repeated")\
        .build()

    if not commands:
        print("No commands provided, using default commands: --version")
        commands = command_builder.queue\
            .add_new_command("version", get_version)\
            .build()
    else:
        if isinstance(commands, list):
            for command in commands:
                command_builder.queue.add_new_command(command.name, command.function, command.args)
            commands = command_builder.build()   
        elif isinstance(commands, Command):
            command_builder.queue.add_new_command(commands.name, commands.function, command.args).build()
        else:
            print("Commands must be a list of Command objects or a single Command object")
            if not commands:
                commands = command_builder.queue\
                    .add_new_command("version", get_version)\
                    .build()
    return commands

def build_parser():
    parserBuilder = ParserBuilder()
    parser = parserBuilder\
        .parser\
            .create_new_args_parser()\
            .add_argument("--version", action="store_true", help="Show version")\
            .add_argument("--repeat", action="store_true", help="Repeat flag")\
        .build()
    
    print("Builder parser: ", parser)
    return parser.get_args_parser()

def use_app_machine(args=None):
    print("using app machine")
    app_machine = AppMachine()
    my_app = app_machine.prepare_default_app()
    print(f"\n->Running sample app: {my_app}")
    my_app.run()
    history = my_app.context.command_queue.get_history()
    print(history)


def main(args=None):
    """Main function for probable_fiesta app.


    Args:
        args (list): List of arguments. Defaults to None.
    """
    # Get args from cli if not provided
    if not args:
        args = sys.argv[1:]

    use_app_machine()

    commands = build_commands()
    context = ContextFactory.new_context(pd.NAME, commands)
    parser = build_parser()
    default_config = get_config()

    main_app = default_app_builder(pd.NAME, context, parser, args, default_config)

    # Get errors
    if main_app.error:
        return main_app.error

    # Run main app
    print(f"\n->Running main app: {main_app}")
    main_app.run()

    # Get command execution history
    history = main_app.context.command_queue.get_history()
    print(history)

    # Return command execution history
    return history

# Get current name and version from config
def get_version() -> str:
    """Get package version.

    Returns:
        str: Current package version.
    """
    return f"{pd.NAME} v.{vd.VERSION}"

def repeat(x):
    return(f"Repeating, {x}")

if __name__ == "__main__":
    main(sys.argv[1:])