from pathlib import Path

import click

from .gpg import main as cmd_gpg
from .ssh import main as cmd_ssh


@click.group(name="export", invoke_without_command=True)
@click.pass_context
@click.option(
    "-p", "--prefix", type=click.Path(file_okay=False, dir_okay=True), default="key"
)
def main(ctx: click.Context, prefix: str | Path) -> None:
    if not ctx.invoked_subcommand:
        prefix = Path(prefix)
        cmd_gpg.main(args=["--prefix", str(prefix / "gpg")], standalone_mode=False)
        cmd_ssh.main(args=["--prefix", str(prefix / "ssh")], standalone_mode=False)
    pass


main.add_command(cmd=cmd_gpg)
main.add_command(cmd=cmd_ssh)
