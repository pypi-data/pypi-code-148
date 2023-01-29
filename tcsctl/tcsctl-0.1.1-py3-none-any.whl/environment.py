from typing import List

from pandas import DataFrame
from tabulate import tabulate
import typer

from . import logger
from .exceptions import TimonApiException
from .models import *

app = typer.Typer()


@app.command("import")
def import_environment(
    ctx: typer.Context,
    name: str,
    repository: str = "thecloudsphere/registry",
    repository_server: str = "https://github.com",
    repository_key: str = None,
):
    try:
        environment = ctx.obj.client.import_environment(
            name,
            repository,
            "environments",
            repository_server,
            repository_key,
            ctx.obj.project_id,
        )
        print(tabulate(environment, headers=["Field", "Value"], tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("list")
def list_environment(
    ctx: typer.Context,
    column: List[str] = typer.Option(
        default=[],
        help="Specify the column(s) to include, can be repeated to show multiple columns",
    ),
):
    try:
        environments = ctx.obj.client.get_environments(ctx.obj.project_id)
        df = DataFrame(
            (x.dict().values() for x in environments),
            columns=Environment.get_field_names(),
        )
        if column:
            result = tabulate(df.filter(items=column), headers=column, tablefmt="psql")
        else:
            result = tabulate(
                df,
                headers=df.columns,
                tablefmt="psql",
            )

        print(result)
    except TimonApiException as e:
        logger.error(str(e))


@app.command("show")
def show_environment(ctx: typer.Context, name: str):
    try:
        environment = ctx.obj.client.get_environment(name, ctx.obj.project_id)
        print(tabulate(environment, headers=["Field", "Value"], tablefmt="psql"))
    except TimonApiException as e:
        logger.error(str(e))


@app.command("edit")
def edit_environment(name: str):
    logger.info("STUB: edit_environment")


@app.command("update")
def update_environment(ctx: typer.Context, name: str):
    ctx.obj.client.update_environment(name, ctx.obj.project_id)


@app.command("delete")
def delete_environment(ctx: typer.Context, name: str):
    try:
        result = ctx.obj.client.delete_environment(name, ctx.obj.project_id)
        print(result)
    except TimonApiException as e:
        logger.error(str(e))
