import typer
from script_master_helper.utils import ProactorServer
from uvicorn import Config

from script_master_ui import const

cli = typer.Typer()


@cli.command()
def run(
    host: str = const.DEFAULT_HOST,
    port: int = const.DEFAULT_PORT,
    debug: bool = const.DEFAULT_DEBUG,
    loglevel: str = const.DEFAULT_LOGLEVEL,
    settings_file: str = None,
):
    # ConfZ automatically reads the CLI parameters.

    from script_master_ui.settings import Settings
    from script_master_ui.routers import app

    hello_text = typer.style(
        "\n===== Script Master UI =====", fg=typer.colors.BRIGHT_YELLOW, bold=True
    )
    typer.echo(hello_text)

    typer.echo(f"HOME DIRECTORY: {const.get_homepath()}")
    typer.echo(f"Swagger: http://{Settings().host}:{Settings().port}/docs")
    typer.echo(f"Api docs: http://{Settings().host}:{Settings().port}/redoc\n")

    for k, v in Settings().dict().items():
        typer.echo(f"{k.upper()}={v}")

    config = Config(
        app=app,
        host=Settings().host,
        port=Settings().port,
        reload=Settings().debug,
        log_level=Settings().loglevel.lower(),
        use_colors=True,
    )
    server = ProactorServer(config=config)
    server.run()
