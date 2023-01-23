

import asyncio
from operator import invert
import websockets
import os
from typing import AsyncGenerator, Tuple, Optional
import qrcode
import socket

from xbridge import bonjour
from xbridge.channel import Channel, ChannelRole
from xbridge.transmsg import NormalMsg
from xbridge.config import Config


async def handle_request(msg: NormalMsg) -> AsyncGenerator[NormalMsg, None]:
    pass


session_count = 0


async def handle_session(websocket):

    try:
        global session_count
        session_count += 1
        print("[+] session count= %d" % session_count)

        print("session start...")
        channel = Channel(ChannelRole.Server)

        # async def subscriber():
        #     async for message in websocket:
        #         yield message

        async def publisher():
            try:
                async for e in channel.publisher():
                    await websocket.send(e)
            finally:
                print("publisher end, now close connection")
                await websocket.close()

        await asyncio.wait([publisher(), channel.subscribe(websocket)])

    finally:
        print("session end!")
        print("close socket")
        await websocket.close()
        session_count -= 1
        print("[-] session count= %d" % session_count)


async def server(name):

    # localhost_pem = os.path.join(Config.config_dir, "cert.pem")
    # print("pem path:", localhost_pem)
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # # localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
    # ssl_context.load_cert_chain(localhost_pem)

    ip = '172.0.0.1'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
        
    try:
        info = None
        async with websockets.serve(
                handle_session,
                "0.0.0.0",
                compression=None,
                ssl=None
        ) as ws:
            # print("ws:", ws.sockets)
            port = ws.sockets[0].getsockname()[1]
            info = bonjour.register_service(name, ip, port)
            name = info.name.split(".")[0]
            print("Server %s run on port %d" % (name, port))

            # show qrcode
            qr = qrcode.QRCode()
            qr.border = 1
            qr.add_data("%s:%d" % (ip, port))
            qr.print_ascii(invert=True)
            await asyncio.Future()  # run forever
    finally:
        if info:
            bonjour.unregister_service(info)
        print("server end")


def start_service(name, dir, fdir=None):

    Config.config_dir = dir
    if not fdir:
        fdir = dir
    Config.files_dir = fdir

    # port = 3000
    # info = bonjour.register_service(name, port)
    # name = info.name.split(".")[0]

    print("service_dir=%s, files_dir=%s" % (dir, fdir))

    # session_dir = os.path.join(Config.service_dir, 'sessions')
    # if os.path.isdir(session_dir):
    #     shutil.rmtree(session_dir, ignore_errors=True)

    if not os.path.exists(dir):
        print('Service dir not exit in %s' % dir)
        return

    if not os.path.exists(fdir):
        os.makedirs(fdir, 0o755)
    elif os.path.isfile(fdir):
        print('Service File dir should be a dir but it is a file! in %s' % fdir)
        return

    try:
        asyncio.run(server(name))
    # except KeyboardInterrupt:
    #     print("keyboard interrupt!")
    # except Exception as e:
    #     print("Server exception: ", e)
    finally:
        print("server end 2")
        pass
