import click

from ..pkg.android_studio.remove import main as android_studio
from ..pkg.cfw.remove import main as cfw
from ..pkg.conda.remove import main as conda
from ..pkg.fonts.remove import main as fonts
from ..pkg.motrix.remove import main as motrix
from ..pkg.zotero.remove import main as zotero


@click.group(name="remove")
def main() -> None:
    pass


main.add_command(cmd=android_studio)
main.add_command(cmd=cfw)
main.add_command(cmd=conda)
main.add_command(cmd=fonts)
main.add_command(cmd=motrix)
main.add_command(cmd=zotero)
