import asyncio
import typer
from rich.console import Console
from rich.live import Live
from rich.table import Table

from aternos.server import connect, get_server

console = Console()
app = typer.Typer()
aternos = connect()


async def _main_start() -> None:
    server = await get_server(aternos)

    if server.status == 'offline':
        console.print(':rocket: Starting server...')
        server.start()
    else:
        console.print('Server is already running :thumbs_up:')

    await connect(server)


async def _main_info() -> None:
    server = await get_server(aternos)
    if server.status != 'offline':
        await connect(server)
    else:
        console.print('Server is offline :rocket:')


async def _main_stop() -> None:
    server = await get_server(aternos)
    server.stop()


@app.command()
def start() -> None:
    asyncio.run(_main_start())


@app.command()
def stop() -> None:
    asyncio.run(_main_stop())


@app.command()
def info() -> None:
    asyncio.run(_main_info())


def tt():
    table = Table("YOLO")
    table.add_row("ouiiii")
    return table


async def _yolo() -> None:
    with Live(tt()) as live_t:
        live_t.update(tt())


@app.command()
def live() -> None:
    asyncio.run(_yolo())
