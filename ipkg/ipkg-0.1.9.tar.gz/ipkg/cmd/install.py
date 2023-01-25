import click

from ..pkg.android_studio.install import main as android_studio
from ..pkg.brew.install import main as brew
from ..pkg.cfw.install import main as cfw
from ..pkg.code.install import main as code
from ..pkg.conda.install import main as conda
from ..pkg.docker.install import main as docker
from ..pkg.edge.install import main as edge
from ..pkg.fonts.install import main as fonts
from ..pkg.motrix.install import main as motrix
from ..pkg.obs.install import main as obs
from ..pkg.reserves_lib_tsinghua_downloader.install import (
    main as reserves_lib_tsinghua_downloader,
)
from ..pkg.typora.install import main as typora
from ..pkg.virtualbox.install import main as virtualbox
from ..pkg.zotero.install import main as zotero


@click.group(name="install")
def main() -> None:
    pass


main.add_command(cmd=android_studio)
main.add_command(cmd=brew)
main.add_command(cmd=cfw)
main.add_command(cmd=code)
main.add_command(cmd=conda)
main.add_command(cmd=docker)
main.add_command(cmd=edge)
main.add_command(cmd=fonts)
main.add_command(cmd=motrix)
main.add_command(cmd=obs)
main.add_command(cmd=reserves_lib_tsinghua_downloader)
main.add_command(cmd=typora)
main.add_command(cmd=virtualbox)
main.add_command(cmd=zotero)
