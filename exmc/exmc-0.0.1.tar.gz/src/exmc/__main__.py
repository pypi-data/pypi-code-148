"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Excel Markdown Converter."""


if __name__ == "__main__":
    main(prog_name="exmc")  # pragma: no cover
