import os

import typer
from script_master_helper.utils import ProactorServer
from uvicorn import Config

from process_executor import const, __version__

cli = typer.Typer()


@cli.command()
def run(
    homedir: str = None,
    host: str = const.DEFAULT_HOST,
    port: int = const.DEFAULT_PORT,
    debug: bool = const.DEFAULT_DEBUG,
    loglevel: str = const.DEFAULT_LOGLEVEL,
    logs_rotation: str = const.DEFAULT_LOGLEVEL,
    logs_retention: str = const.DEFAULT_LOGLEVEL,
    settings_file: str = None,
):
    # ConfZ automatically reads the CLI parameters.

    if homedir:
        os.environ[const.HOME_DIR_VARNAME] = homedir

    from process_executor.app import app
    from process_executor.settings import Settings

    hello_text = typer.style(
        f"===== Process Executor {__version__} =====", fg=typer.colors.BRIGHT_YELLOW
    )
    typer.echo(hello_text)

    typer.echo(f"HOME DIRECTORY: {const.get_homepath()}")
    typer.echo(f"Swagger: http://{Settings().host}:{Settings().port}/docs")
    typer.echo(f"Api docs: http://{Settings().host}:{Settings().port}/redoc\n")

    for k, v in Settings().dict().items():
        typer.echo(f"{k.upper()}={v}")

    Settings().scripts_dir.mkdir(exist_ok=True)
    Settings().logs_dir.mkdir(exist_ok=True)
    Settings().process_log_dir.mkdir(exist_ok=True)

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
