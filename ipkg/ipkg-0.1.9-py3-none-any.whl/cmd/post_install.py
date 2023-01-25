import click

from ..pkg.android_studio.post_install import main as android_studio
from ..pkg.gh.post_install import main as gh


@click.group(name="post-install")
def main() -> None:
    pass


main.add_command(cmd=android_studio)
main.add_command(cmd=gh)
