import click

from .apt import main as cmd_apt
from .brew import main as cmd_brew
from .ignore_io import main as cmd_ignore_io
from .snap import main as cmd_snap
from .tldr import main as cmd_tldr


@click.group(name="update", invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    if not ctx.invoked_subcommand:
        for name, cmd in main.commands.items():
            ctx.invoke(cmd)


main.add_command(cmd=cmd_apt)
main.add_command(cmd=cmd_brew)
main.add_command(cmd=cmd_ignore_io)
main.add_command(cmd=cmd_snap)
main.add_command(cmd=cmd_tldr)
