
import asyncio
from typing import Tuple, Optional
import websockets

from xbridge import bonjour
from xbridge.channel import Channel, ChannelRole
from xbridge.transmsg import NormalMsg


def get_service_ip_port(service_name: str) -> Optional[Tuple[str, str]]:
    print("search service %s" % service_name)
    info = bonjour.get_service_info(service_name)
    if info is None:
        print("can't find service %s" % service_name)
        return None
    return bonjour.get_ip_port(info)
    # print("service address: %s%d" % ('ws://' + ip + ':', port))

    # return (ip, port)


def get_service_url(service_name: str):
    url = 'http://'
    name_arr = service_name.split(':')
    if len(name_arr) == 2:
        url += service_name
    else:
        (ip, port) = get_service_ip_port(service_name)
        url += ('%s:%d' % (ip, port))

    print('url: ', url)

    return url


def get_service_url(service_name: str):
    url = 'ws://'
    name_arr = service_name.split(':')
    if len(name_arr) >= 2:
        url += service_name
    else:
        (ip, port) = get_service_ip_port(service_name)
        url += ('%s:%d' % (ip, port))

    print('url: ', url)

    return url

async def do_request(service_name, msg: NormalMsg, handle_reply):
    url = get_service_url(service_name)

    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # localhost_pem = os.path.join(Config.config_dir, "cert.pem")
    # ssl_context.load_cert_chain(localhost_pem)
    # ssl_context.check_hostname = False
    # ssl_context.verify_mode = ssl.VerifyMode.CERT_NONE

    async with websockets.connect(url, compression=None, ssl=None) as websocket:

        try:
            print("session start...")
            channel = Channel(ChannelRole.Client)

            # async def subscriber():
            #     async for message in websocket:
            #         yield message

            async def publisher():
                try:
                    async for data in channel.publisher(msg, handle_reply):
                        await websocket.send(data)
                finally:
                    print("publisher end, now close connection")
                    await websocket.close()

            await asyncio.wait([publisher(), channel.subscribe(websocket)])

        finally:
            print("close socket")
            await websocket.close()
            print("session end!")



# async def do_request_info(service_name: str):

#     url = get_service_url(service_name)
#     msg = NormalMsg(MsgType.GetInfo)
#     async with websocket_client(url) as client:
#         result = await client.request_response(Payload(msg.toBytes()))
#         ret = NormalMsg.fromBytes(result.data)
#         # print(ret.toString())
#         print("Service Supported Actions:")
#         if ret.params:
#             for item in ret.params:
#                 print("\t%s" % item)
#         else:
#             print('nothing!!!')


def request(service_name, msg, handle_reply):
    try:
        asyncio.run(do_request(service_name, msg, handle_reply))
    # except KeyboardInterrupt:
    #     print("keyboard interrupt")
    # except Exception as e:
    #     print("Client exception:", e)
    finally:
        pass


# def request_info(service_name):
#     try:
#         asyncio.run(do_request_info(service_name))
#     # except KeyboardInterrupt:
#     #     print("keyboard interrupt!")
#     # except Exception as e:
#     #     print("Client exception: ", e)
#     finally:
#         pass

# def game_make_select():
#     action_type = 1
#     content = "hello"
#     # length = len(content)

#     type_bytes = action_type.to_bytes(4, 'little', signed=False)
#     content_bytes = bytes(content, encoding='utf8')
#     length = len(content_bytes)
#     length_bytes = length.to_bytes(4, 'little', signed=False)
#     return type_bytes + length_bytes + content_bytes


# def game_make_move():
#     action_type = 2
#     pass


# async def test_game(service_name):
#     url = get_ws_url(service_name)
#     try:
#         async with websockets.connect(url) as websocket:

#             data = game_make_select()

#             await websocket.send(data)

#             print("waiting for msg")
#             # async for message in websocket:
#             #     print('recv:', message)
#             #     #await process(message)

#             msg = await websocket.recv()
#             print('recv:', msg)

#     except websockets.exceptions.ConnectionClosedError as e:
#         print(e)

#     pass


# def test(service_name):
#     print(service_name)
#     asyncio.run(test_game(service_name))
