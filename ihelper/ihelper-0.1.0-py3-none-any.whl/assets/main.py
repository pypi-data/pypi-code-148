import click

from .avatar import main as cmd_avatar
from .favicon import main as cmd_favicon


@click.group(name="assets", invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    if not ctx.invoked_subcommand:
        for name, cmd in main.commands.items():
            ctx.invoke(cmd)


main.add_command(cmd=cmd_avatar)
main.add_command(cmd=cmd_favicon)
