import _toori

import socket
import asyncio
import socketio
from concurrent.futures import ThreadPoolExecutor

# Increase the packet buffer
from engineio.payload import Payload

Payload.max_decode_packets = 2500000

_executor = ThreadPoolExecutor(1)

sio = socketio.AsyncClient()

loop = asyncio.get_event_loop()

LOCAL_IP = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

def resolve_address(address):
    hostname = address.split("//")[-1:][0]
    ip = socket.gethostbyname(hostname)

    return ip


@sio.on("message")
async def print_message(msg):
    print(msg)


@sio.on("designate")
async def designate(virtual_ip):
    print(f"Virtual address: {virtual_ip}")


@sio.on("connect")
async def on_connect():
    print("connected to server")


@sio.on("in")
async def handle_incoming(data):
    # await loop.run_in_executor(_executor, _toori.inj, data)
    _toori.inj(data)
    # await asyncio.sleep(0.0)


async def start_client(address, requested_ip, filter_string):
    headers = {"req_ip": requested_ip, "loc_ip": LOCAL_IP}

    try:
        await sio.connect(f"{address}", auth=headers)
    except socketio.exceptions.ConnectionError:
        print(f"Unable to connect to the address {address}")
        exit()

    _toori.init(
        filter_string,
        LOCAL_IP,
    )

    while True:
        data = await loop.run_in_executor(_executor, _toori.get)
        # data = _toori.get()
        if len(data) > 0:
            try:
                await sio.emit(event="out", data=data)
            except Exception:
                pass

        # await asyncio.sleep(0.0001)


def start(address, filter_string=None, requested_ip=None, no_dns=False):
    if filter_string is None:
        filter_string = f"outbound && !loopback && ip.DstAddr != {resolve_address(address)} && ip"

    if no_dns:
        filter_string = f"outbound && !loopback && ip.DstAddr != {resolve_address(address)} && (tcp || udp.DstPort != 53 || icmp)"

    try:
        loop.run_until_complete(start_client(address, requested_ip, filter_string))
    except KeyboardInterrupt:
        _toori.stop()
        print("Exited, have a nice day :)")
