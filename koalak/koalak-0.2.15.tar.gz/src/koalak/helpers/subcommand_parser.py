import argparse
import inspect
import sys
import typing

import argcomplete
import attrs
import coloring
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# RICH STYLE CONSTS

STYLE_OPTIONS_TABLE_SHOW_LINES = False
STYLE_OPTIONS_TABLE_LEADING = 0
STYLE_OPTIONS_TABLE_PAD_EDGE = False
STYLE_OPTIONS_TABLE_PADDING = (0, 1)
STYLE_OPTIONS_TABLE_BOX = ""
STYLE_OPTIONS_TABLE_ROW_STYLES = None
STYLE_OPTIONS_TABLE_BORDER_STYLE = None
STYLE_OPTION = "bold cyan"

UNGROUPED_NAME = "_ungrouped"
UNGROUPED_TITLE_WHEN_MANY_GROUP = "Other commands"
UNGROUPED_TITLE_WHEN_ONE_GROUP = "Commands"


console = Console()


@attrs.define
class Argument:
    dest: str = attrs.field()
    help: str = attrs.field()
    required: bool = attrs.field()
    name: attrs.field()
    is_option: bool = attrs.field()


def argparse_argument_to_subcommand_argument(argparse_action):
    dest = argparse_action.dest
    help = argparse_action.help
    if argparse_action.option_strings == []:
        required = True
        name = dest
        is_option = False
    else:
        required = False
        name = " ".join(argparse_action.option_strings)
        is_option = True
    return Argument(
        dest=dest, help=help, required=required, name=name, is_option=is_option
    )


class SubcommandParser:
    def __init__(
        self,
        prog=None,
        *,
        parent=None,
        parser=None,
        autocomplete: bool = None,
        # Help
        prolog=None,
        description=None,
        epilog=None,
    ):
        """

        Args:
            prog: name of the program
            parent: parent parser
            parser: argparse.ArgParser to use
            description: description of the program
            autocomplete: E,able autocomplete

        Advantages over argparse:
            - use add_subcommand instead of using add_parsers then add_subparser
            - run command that will run directly the program
            - better help with groups/colors
            - ease of use autocomplete
        """

        # FIXME: if parser is given don't take prolog/epilog
        if prog is None:
            prog = sys.argv[0]

        if autocomplete is None:
            autocomplete = False

        self.parent = parent
        self.name = prog or sys.argv[0]
        self.subcommands: typing.Dict[str, SubcommandParser] = {}
        self.function = None  # function to run
        self._argparse_subparsers = None

        # Help related attributes
        self.groups = {}
        self.add_group(UNGROUPED_NAME, title=UNGROUPED_TITLE_WHEN_MANY_GROUP)
        self.description = description
        self.prolog = prolog
        self.epilog = epilog
        self.hide = False
        self.autocomplete = autocomplete
        # FIXME: _group_namespace usage
        self._group_namespace = (
            set()
        )  # track groupnamespace for subcommands and help_subcommands

        if self.parent is None:
            self.fullname = self.name
        else:
            self.fullname = f"{self.parent.fullname}.{self.name}"

        if parser is None:
            parser = argparse.ArgumentParser(
                prog=prog, description=description, epilog=epilog
            )

        self._argparse_parser = parser
        self._subcommand_depth = 1

        self._argparse_parser.print_help = self.print_help

    def add_argument(self, *args, **kwargs):
        self._argparse_parser.add_argument(*args, **kwargs)

    def add_group(self, name, *, title: str = None, description: str = None):
        if name in self.groups:
            raise KeyError(f"Group {name} already exists")

        if title is None:
            title = name

        if description is None:
            description = ""

        self.groups[name] = CommandsGroup(
            name=name, title=title, description=description
        )

    def add_subcommand(self, command_name, description=None, group=None, hide=False):
        if command_name in self.subcommands:
            raise KeyError(f"command {command_name!r} already exists")

        # TODO: check that help_command is not existing in the same grp
        #  refactor this! we should check all namespace not only the one for grp
        # TODO: test me

        # FIXME: move hide in print
        if not hide:
            if command_name in self._group_namespace:
                raise KeyError(
                    f"command {command_name!r} already exists as help_subcommand"
                )

        if group is None:
            group = UNGROUPED_NAME

            self._group_namespace.add(command_name)

        if self._argparse_subparsers is None:
            self._argparse_subparsers = self._argparse_parser.add_subparsers(
                dest=self._get_subcommand_dest_name()
            )

        subcommand_parser = self._argparse_subparsers.add_parser(command_name)

        subcommand_command = SubcommandParser(
            command_name,
            parser=subcommand_parser,
            parent=self,
            description=description,
        )
        # Add it to group
        self.groups[group].commands[command_name] = subcommand_command

        subcommand_command._subcommand_depth += self._subcommand_depth
        subcommand_command.hide = hide

        # Add it to subcommands
        self.subcommands[command_name] = subcommand_command
        return subcommand_command

    def add_help_subcommand(self, command_name, description=None, group=None):
        """Only add this command in the help

        Explanation:
            this could be useful if you have a lot of commands that are hidden
            and you want to add one help description to group all these commands
        """
        # FIXME
        if group is None:
            group = UNGROUPED_NAME

        if command_name in self.subcommands:
            raise KeyError(f"command {command_name!r} already exists")

        if command_name in self._group_namespace:
            raise KeyError(
                f"command {command_name!r} already exists in help_subcommands"
            )

        self.groups[group]["commands"][command_name] = {"description": description}
        self._group_namespace.add(command_name)

    def __getitem__(self, item: str):
        return self.subcommands[item]

    def __str__(self):
        return f"SubcommandParser(<{self.fullname}>)"

    def __repr__(self):
        return self.__str__()

    def parse_args(self, args=None, namespace=None):
        self.check_errors()

        if self.autocomplete:
            argcomplete.autocomplete(self._argparse_parser)

        return self._argparse_parser.parse_args(args, namespace=namespace)

    def run(self, args=None):
        """Run the main program"""

        # Parse arguments
        parsed_args = self.parse_args(args)
        # TODO: hook main: self._run_main(parsed_args)  # hook to _run_main

        # Check if there is any subcommand
        if not self.subcommands:
            self.print_help()
            sys.exit(1)

        # get called subcommand
        depth = 1
        subcommand = self
        while True:
            try:

                cmd_name = self._get_subcommand_name(parsed_args, depth=depth)

                if cmd_name is None:
                    self.print_help()
                    sys.exit(1)
                subcommand = subcommand[cmd_name]
                depth += 1
            except AttributeError:
                break

        # If function is None, automatically it (doesn't have subparsers
        #  because we already checked errors on parse_args
        if subcommand.function is None:
            self.print_help()
            sys.exit(0)

        subcommand.function(parsed_args)

    def _get_rich_table(self):
        t_styles: typing.Dict[str, typing.Any] = {
            "show_lines": STYLE_OPTIONS_TABLE_SHOW_LINES,
            "leading": STYLE_OPTIONS_TABLE_LEADING,
            "box": STYLE_OPTIONS_TABLE_BOX,
            "border_style": STYLE_OPTIONS_TABLE_BORDER_STYLE,
            "row_styles": STYLE_OPTIONS_TABLE_ROW_STYLES,
            "pad_edge": STYLE_OPTIONS_TABLE_PAD_EDGE,
            "padding": STYLE_OPTIONS_TABLE_PADDING,
        }
        return Table(
            highlight=True,
            show_header=False,
            expand=True,
            **t_styles,
        )

    def print_help(self, file=None):
        """If groups exist change the current help"""
        """
        - prolog
        - usage
        - prog description
        - list subcommands
        - epilog
        """
        usage_style = "yellow bold"

        options = []
        arguments = []
        for action in self._argparse_parser._actions:
            argument = argparse_argument_to_subcommand_argument(action)
            if argument.is_option:
                options.append(argument)
            else:
                if argument.name.startswith("subcommand"):
                    continue
                arguments.append(argument)

        # FIXME: test/me
        # Handle groups
        # =============
        # Groups are already handled in add_subcommand
        if len(self.groups) == 1:
            # If len groups == 1, title = "Commands" else title = "Other commands"
            self.groups[UNGROUPED_NAME].title = "Commands"
        else:
            self.groups[UNGROUPED_NAME].title = "Other commands"

        # make ungrouped in last position
        _ungrouped = self.groups.pop(UNGROUPED_NAME)
        self.groups[UNGROUPED_NAME] = _ungrouped

        # header prog name and description
        prog = self.name

        # add prolog
        if self.prolog:
            console.print(self.prolog)

        # Print usage
        console.print(f"[{usage_style}]Usage:[/{usage_style}] {prog} [-h] <subcommand>")
        console.print()

        # add description
        if self.description:
            console.print(f"{self.description}")
            console.print()

        # from devtools import debug
        for group_name, group in self.groups.items():
            if not group.commands:
                continue

            # Taken from typer
            # FIXME: add description
            options_table = self._get_rich_table()
            for cmd_name, command in group.commands.items():
                cmd_name = Text(cmd_name, style=STYLE_OPTION)
                options_table.add_row(cmd_name, command.description)

            group_panel = Panel(
                options_table, title=group.title, border_style="dim", title_align="left"
            )
            console.print(group_panel)

        # Print arguments
        if arguments:
            options_table = self._get_rich_table()
            for option in arguments:
                options_table.add_row(option.name, option.help)
            group_panel = Panel(
                options_table, title="Arguments", border_style="dim", title_align="left"
            )
            console.print(group_panel)

        # Print options
        if options:
            options_table = self._get_rich_table()
            for option in options:
                options_table.add_row(option.name, option.help)
            group_panel = Panel(
                options_table, title="Options", border_style="dim", title_align="left"
            )
            console.print(group_panel)

        if self.epilog:
            console.print(self.epilog)
        # change the help function

    def __call__(self, function):
        self.function = function

    def iter_allcommands(self):
        """Iter all commands, self included"""
        yield self
        for parser in self.subcommands.values():
            yield from parser.iter_allcommands()

    def check_errors(self):
        """Check if subcommands are correctly built
        This method is called before parse_args/run
        """
        for command in self.iter_allcommands():
            # If function exists it must be callable
            if command.function is not None and not callable(command.function):
                raise TypeError(f"{command.fullname}.function must be callable")

            # Todo: check that function has only one argument

            # If the command don't have any subcommand, it must have a function
            if not command.subcommands and command.function is None:
                raise ValueError(
                    f"Subcommand {command} don't have linked function or should have subpcommands"
                )

    # Private methods #
    # =============== #
    def _get_subcommand_dest_name(self, depth: int = None):
        if depth is None:
            depth = self._subcommand_depth
        if depth == 1:
            return "subcommand"
        else:
            return f"subcommand_{depth}"

    def _get_subcommand_name(self, parsed_args, depth: int = None):
        argparse_cmd_name = self._get_subcommand_dest_name(depth)
        return getattr(parsed_args, argparse_cmd_name)

    def _print_and_exist(self, msg, status=1):
        print(msg)
        sys.exit(status)


@attrs.define
class CommandsGroup:
    name: str = attrs.field()
    title: str = attrs.field()
    description: str = attrs.field(default=None)
    commands: typing.Dict[str, SubcommandParser] = attrs.field(factory=dict)


# TODO: deprecate old argparse
# TODO: add help feature
# TODO: groups with help
