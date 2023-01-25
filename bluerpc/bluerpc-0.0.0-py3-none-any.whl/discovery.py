import socket

from bluerpc.utils import get_version
from zeroconf import IPVersion
from zeroconf.asyncio import AsyncServiceInfo, AsyncZeroconf


async def start_discovery(
    bind_addr: str = "[::]:50052",
    name: str = "unknown",
    encrypted: bool = False,
) -> None:
    """
    Start the mDNS task for auto-discovery

    Args:
        bind_addr: the bind address passed to the worker
        name: the name of the worker
        encrypted: if the worker is running with encryption
    """
    aiozc = AsyncZeroconf(ip_version=IPVersion.All)
    await aiozc.async_register_service(
        AsyncServiceInfo(
            "_bluerpc._tcp.local.",
            f"{name}._bluerpc._tcp.local.",
            addresses=[socket.gethostbyname_ex(socket.gethostname())[2][-1]],
            port=int(bind_addr[bind_addr.rfind(":") + 1:]),
            properties={"encrypted": encrypted, "name": name, "version": get_version()},
        )
    )
