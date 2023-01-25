import click

from .secret.main import main as cmd_secret


@click.group(name="git")
def main() -> None:
    pass


main.add_command(cmd=cmd_secret)
