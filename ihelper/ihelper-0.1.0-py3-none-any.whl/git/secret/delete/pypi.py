import click

from ..utils import gh_secret_delete


@click.command(name="pypi")
@click.option(
    "-R",
    "--repo",
    metavar="[HOST/]OWNER/REPO",
    help="Select another repository using the [HOST/]OWNER/REPO format",
)
def main(repo: str) -> None:
    gh_secret_delete(name="PYPI_USERNAME", repo=repo)
    gh_secret_delete(name="PYPI_PASSWORD", repo=repo)
