"""CLI test commands"""

import asyncio
import click
from eze.utils.click.command_helpers import base_options, pass_state
from eze.core.engine import EzeCore


@click.command("test")
@base_options
@pass_state
@click.option(
    "--scan-type",
    "-s",
    help="named custom scan type to run aka production can include run type aka 'safety:test-only'",
    required=False,
)
@click.option(
    "--tool",
    "-t",
    help="named tool to run aka 'semgrep'",
    required=False,
)
@click.option(
    "--force-autoscan/--dont-force-autoscan",
    help="Forces language autoscan and creation of new .ezerc.toml",
    default=False,
)
@click.option("--autoconfig", type=click.Path(exists=True), help="File with custom autoconfig json", required=False)
def test_command(
    state,
    config_file: str,
    scan_type: str = "",
    tool: str = "",
    force_autoscan: bool = False,
    autoconfig: click.Path = None,
) -> None:
    """Eze run scan"""
    EzeCore.auto_build_ezerc(force_autoscan, autoconfig)
    eze_core = EzeCore.get_instance()
    asyncio.run(eze_core.run_scan(scan_type=scan_type, custom_tools=[tool] if tool else None))
