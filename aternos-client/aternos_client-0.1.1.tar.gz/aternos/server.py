import asyncio
import time

from python_aternos import AternosServer, Client, Streams
from typing import Tuple, Dict, Any, List

from rich.console import Console
from rich.live import Live
from rich.prompt import Prompt, IntPrompt
from rich.table import Table


console = Console()

list_players = []


async def get_server(aternos: Client) -> AternosServer:
    _show_servers(aternos.list_servers())
    server_choose = IntPrompt.ask("Select server", default=0)
    server: AternosServer = aternos.list_servers()[server_choose]
    return server


def connect() -> Client:
    try:
        aternos = Client.restore_session()
    except FileNotFoundError:
        user = Prompt.ask("Enter the login")
        password = Prompt.ask("Enter the password", password=True)
        aternos = Client.from_credentials(user, password)
        aternos.save_session()
    return aternos


async def connect(server: AternosServer) -> None:
    with Live(_show_players([]), refresh_per_second=4) as live:
        await _socket_connect(server, live)


async def _socket_connect(server: AternosServer, live: Live) -> None:
    socket = server.wss()

    @socket.wssreceiver(Streams.status, ('Server 1',))
    async def state(
            msg: Dict[Any, Any],
            args: Tuple[str]) -> None:
        server._info = msg
        # console.print(args)
        # _show_server(server)
        # _show_players(server.players_list)
        live.update(_show_players(server.players_list))

    await socket.connect()
    await asyncio.create_task(_loop())


def _show_servers(servers: List[AternosServer]) -> None:
    table = Table("#", "Server", "Version", "Status")
    for index, server in enumerate(servers):
        table.add_row(str(index), server.address, server.version, server.status)
    console.print(table)


def _show_server(server: AternosServer) -> None:
    table = Table("#", "Server", "Version", "Status")
    table.add_row("0", server.address, server.version, server.status)
    console.print(table)


def _show_players(players: List[str]) -> None:
    table = Table("Players online")
    for player in players:
        table.add_row(player)
    console.print(table)


async def _loop() -> None:
    while True:
        await asyncio.Future()
