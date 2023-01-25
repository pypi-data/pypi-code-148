import subprocess

import click
from ishutils.common.run import run

from ..utils import gh_secret_set


@click.command(name="pypi")
@click.option(
    "-R",
    "--repo",
    metavar="[HOST/]OWNER/REPO",
    help="Select another repository using the [HOST/]OWNER/REPO format",
)
@click.option("-u", "--username", default="liblaf")
@click.option("-p", "--password")
def main(repo: str, username: str, password: str) -> None:
    if not password:
        password = str(
            run(args=["bw", "get", "password", "PyPI"], stdout=subprocess.PIPE).stdout,
            encoding="utf-8",
        )
    gh_secret_set(name="PYPI_USERNAME", body=username, repo=repo)
    gh_secret_set(name="PYPI_PASSWORD", body=password, repo=repo)
