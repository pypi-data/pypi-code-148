""""Main module for probable_fiesta app."""
import sys

from ..config.variables import PackageDef as pd
from ..config.variables import VariablesDef as vd
from ..app.builder.app_builder import AppBuilder
from ..app.builder.context import Context
from ..command.builder.command_builder import CommandBuilder
from ..config.default_config import get_config
from ..command.builder.command import Command
from ..app.builder.app_abstract_machine import AppMachine
from ..cli.builder.parser_builder import ParserBuilder
from ..command.builder.command_factory import CommandFactory
from ..command.builder.command_queue import CommandQueue
from ..cli.builder.args_parse import Parser


def use_app_machine(args=None):
    print("using app machine")
    app_machine = AppMachine()
    my_app = app_machine.prepare_default_app()
    print(f"\n->Running sample app: {my_app}")
    #my_app.run()
    #history = my_app.context.command_queue.get_history()
    #print(history)


def main(args=None):
    """Main function for probable_fiesta app.


    Args:
        args (list): List of arguments. Defaults to None.
    """
    # Get args from cli if not provided
    if not args:
        args = sys.argv[1:]

    default_config = get_config(log_name="probable_fiesta")

    aB = AppBuilder()
    # [oui_la_la], ["oui la la"]
    clean_args, clean_argv = aB.arguments.clean_arg_function(args)
    if len(clean_argv) == 0:
        clean_argv.append(None)


    aB = AppBuilder()
    main_app = aB\
        .name\
            .set_name("main_app")\
        .arguments\
            .set_arguments(args)\
        .args_parser\
            .add_argument("--test-app", type=str, help="test app builder")\
            .add_argument("--version", action='store_true', help="show version builder")\
            .add_argument("--repeat", type=str, help="repeat input")\
        .context\
            .add_context(Context.Factory().new_context(
                "test_app",
                CommandQueue.new(
                    [CommandFactory.new_command("test_app_func", lambda x: x, "repeated")]
                )))\
            .add_context(Context.Factory().new_context(
                "version",
                CommandQueue.new(
                    [CommandFactory.new_command("version", get_version, None)]
                )))\
            .add_context(Context.Factory().new_context(
                "repeat",
                CommandQueue.new(
                    [CommandFactory.new_command("repeat", repeat, args=clean_argv[0])]
                )))\
        .config\
            .set_config(default_config)\
        .validate()\
        .build()
    #print(main_app)

    #use_app_machine()

    # Get parser error
    if main_app.args_parser.error:
        return main_app.args_parser.error

    # Run main app
    #print(f"\n->Running main app: {main_app}")
    #print("WILL RUN COMMANDS:", main_app.cleaned_args)
    for command in main_app.cleaned_args:
        main_app.run(command)

    # Create second argument parser
    #pa = main_app.args_parser.get_parsed_args()
    #print(pa)
    #validated = vars(pa)
    #print(validated)
    #keys = validated.keys()
    #print("keys: ", keys)
    #print("VS ARGS: ", args)
    #tmp_parser = Parser.Factory.new()
    #my_args = tmp_parser.parser.parse_args(args)
    #print("My Args PARSER: ", my_args)
    #my_args = vars(my_args)
    #for command in my_args.keys():
        #print("command: ", command)
        #main_app.run(command)

    # Get command execution history
    #history = main_app.context.command_queue.get_history()
    #print(history)

    # Get command execution history new
    history_new = main_app.get_run_history()
    print(history_new)

    # Return command execution history
    return history_new

# Get current name and version from config
def get_version() -> str:
    """Get package version.

    Returns:
        str: Current package version.
    """
    return f"{pd.NAME} v.{vd.VERSION}"

def repeat(x):
    return(f"Repeating: {x}")

if __name__ == "__main__":
    main(sys.argv[1:])