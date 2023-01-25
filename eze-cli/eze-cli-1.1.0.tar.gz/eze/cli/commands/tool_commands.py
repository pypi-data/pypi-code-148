"""CLI tools command"""

import sys

import click

from eze.utils.click.command_helpers import debug_option
from eze.utils.vo.enums import SourceType
from eze.core.tool import ToolManager, ToolType
from eze.utils.log import log


@click.group("tools")
@debug_option
def tools_group():
    """container for tool commands"""


@click.command("list", short_help="List the available tools")
@click.option("--tool-type", "-t", help=f"filter by tool type ({','.join(ToolType.__members__)})")
@click.option("--source-type", "-s", help=f"filter by source type ({','.join(SourceType.__members__)})")
@click.option("--include-source-type/--exclude-source-type", default=False, help="adds source type column")
@click.option(
    "--include-version/--exclude-version",
    default=False,
    help="""adds version column
(slow as needs to collect all software versions of tools)""",
)
@click.option("--include-help/--exclude-help", default=False, help="adds all tools documentation")
@debug_option
def list_command(
    tool_type: str, source_type: str, include_source_type: bool, include_version: bool, include_help: bool
) -> None:
    """
    list available tools
    """
    if tool_type and tool_type not in ToolType.__members__:
        log(f"Could not find tool type '{tool_type}'")
        log(f"Available tool types are ({','.join(ToolType.__members__)})")
        sys.exit(1)

    if source_type and source_type not in SourceType.__members__:
        log(f"Could not find source type '{source_type}'")
        log(f"Available source types are ({','.join(SourceType.__members__)})")
        sys.exit(1)

    tool_manager: ToolManager = ToolManager.get_instance()
    tool_manager.print_tools_list(tool_type, source_type, include_source_type, include_version)
    if include_help:
        tool_manager.print_tools_help(tool_type, source_type, include_source_type)


@click.command("help", short_help="List the help for a given tool")
@click.argument("tool", required=True)
@debug_option
def help_command(tool: str) -> None:
    """
    display help for selected tool
    """
    tool_manager = ToolManager.get_instance()
    if tool not in tool_manager.tools:
        log(f"Could not find tool '{tool}', use 'eze tools list' to get available tools")
        sys.exit(1)

    tool_manager.print_tool_help(tool)


tools_group.add_command(list_command)
tools_group.add_command(help_command)
