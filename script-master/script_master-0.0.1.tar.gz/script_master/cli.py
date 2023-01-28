import os
from os.path import abspath
from pathlib import Path

import jinja2
import typer
from uvicorn import Config

import process_executor.const
from script_master import const
from script_master_helper.utils import ProactorServer

cli = typer.Typer()


@cli.command()
def init(path: str = None):
    """Create .env file"""

    directory = Path(abspath(__file__)).parent
    with open(directory / "template-settings.env") as f:
        template = jinja2.Template(f.read())

    data = {
        "python_version": process_executor.const.DEFAULT_PYTHON_VERSION,
        "cpu_count": process_executor.const.MAX_PROCESSES,
    }

    home_dir = Path(path or Path.cwd())
    os.environ[const.HOME_DIR_VARNAME] = str(home_dir)

    template.stream(environ=os.environ, **data).dump(str(home_dir / ".env"))


@cli.command()
def run(
    homedir: str = None,
    host: str = const.DEFAULT_HOST,
    port: int = const.DEFAULT_PORT,
    debug: bool = const.DEFAULT_DEBUG,
    loglevel: str = const.DEFAULT_LOGLEVEL,
    settings_file: str = None,
):
    # ConfZ automatically reads the CLI parameters.

    if homedir:
        os.environ[const.HOME_DIR_VARNAME] = homedir

    from script_master.settings import Settings
    from script_master.resources import app

    hello_text = typer.style(
        "\n===== Script Master =====", fg=typer.colors.BRIGHT_YELLOW, bold=True
    )
    typer.echo(hello_text)

    typer.echo(f"HOME DIRECTORY: {const.get_homepath()}")
    typer.echo(f"Swagger: http://{Settings().host}:{Settings().port}/docs")
    typer.echo(f"Api docs: http://{Settings().host}:{Settings().port}/redoc\n")

    for k, v in Settings().dict().items():
        typer.echo(f"{k.upper()}={v}")

    const.get_homepath().mkdir(exist_ok=True)
    Path(Settings().VARIABLES_DIR).mkdir(exist_ok=True)
    Path(Settings().NOTEBOOK_DIR).mkdir(exist_ok=True)
    Path(Settings().ARCHIVE_NOTEBOOK_DIR).mkdir(exist_ok=True)
    Path(Settings().LOGS_DIR).mkdir(exist_ok=True)

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
