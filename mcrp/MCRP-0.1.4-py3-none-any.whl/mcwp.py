"""
    MineCraft Watching Proxy
    ========================
"""

from MCRP import MCRewriteProxy, Relative, version
import cubelib

from ruamel.yaml import YAML
import argparse
import logging
from .util import CustomFormatter

BANNER = \
f"""
 __  __   ____  ____   ____       __        __ ____
|  \/  | / ___||  _ \ |  _ \  _   \ \      / /|  _ \\
| |\/| || |    | |_) || |_) |(_)   \ \ /\ / / | |_) |
| |  | || |___ |  _ < |  __/  _     \ V  V /  |  __/
|_|  |_| \____||_| \_\|_|    (_)     \_/\_/   |_| v{version}
"""

def main():

    print(BANNER[1:])
    parser = argparse.ArgumentParser(description="Minecraft Watching Proxy")
    parser.add_argument("-c", type=argparse.FileType("r", encoding="utf-8"), help="Path to YAML config file", metavar="config.yaml")
    parser.add_argument("-v", action="store_true", help="If passed, enables verbose logging")
    parser.add_argument("-l", help="Proxy listen addr [localhost:25565] (enclose ipv6 like [::])", default="127.0.0.1:25565", metavar="addr")
    parser.add_argument("-u", help="Proxy upstream server addr [localhost:25575]", default="127.0.0.1:25575", metavar="addr")
    args = parser.parse_args()
    
    if args.c:
        yaml = YAML(typ="safe")
        conf = yaml.load(args.c)
    else:
        conf = {"mode": "blacklist"}

    def host2ap(addr: str):
        x = addr.split(']')
        if len(x) == 2:
            return x[0]+']', int(x[1][1:])
        x = addr.split(":")
        return x[-2], int(x[-1])

    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG if args.v else logging.INFO)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter('[%(asctime)s] [%(levelname)s] %(name)s:  %(message)s'))
    logger.addHandler(stdout_handler)

    limit = conf["loglimit"] if "loglimit" in conf else None
    if "mode" in conf:
        cbmode = conf["mode"]
        sbmode = conf["mode"]
    elif "ClientBoundMode" in conf and "ServerBoundMode" in conf:
        cbmode = conf["ClientBoundMode"]
        sbmode = conf["ServerBoundMode"]
        conf["mode"] = f"ClB: {cbmode} / SvB: {sbmode}"
    else:
        logger.error(f"Failed to read configuration! please declate 'mode' or 'ClientBoundMode' and 'ServerBoundMode'")
        exit()

    proxy = MCRewriteProxy(host2ap(args.l), host2ap(args.u), logging.INFO if args.v else logging.ERROR)

    ClientBoundFilterList = []
    ServerBoundFilterList = []

    @proxy.on(cubelib.proto.ServerBound.Handshaking.Handshake)
    def handler(packet):
        nonlocal ClientBoundFilterList, ServerBoundFilterList

        if packet.NextState != cubelib.NextState.Login:
            return

        logger.debug(f'Selected proto version is: {packet.ProtoVer}, building filter...')
        proto = proxy.PROTOCOL

        def find_ap_by_path(proto, path):
            obj = proto
            attrs = path.split('.')
            if attrs[-1] == "NotImplementedPacket":
                return cubelib.p.NotImplementedPacket

            for attr in attrs:
                obj = getattr(obj, attr, None)
                if not obj:
                    logger.debug(f'\x1b[38;5;226mFailed to resolve filter packet {proxy.PROTOCOL.__name__}.{".".join(attrs)}')
                    break
            return obj
        
        ClientBoundFilterList = [find_ap_by_path(proto, "ClientBound.Play." + packet) for packet in conf["ClientBound"]] if "ClientBound" in conf else []
        ServerBoundFilterList = [find_ap_by_path(proto, "ServerBound.Play." + packet) for packet in conf["ServerBound"]] if "ServerBound" in conf else []
        ClientBoundFilterList = [i for i in ClientBoundFilterList if i is not None]
        ServerBoundFilterList = [i for i in ServerBoundFilterList if i is not None]

        logger.debug(f"Filtering mode: {conf['mode']}, filtered packets:")

        logger.debug(f"ClientBound [{len(ClientBoundFilterList)}]:")
        for packet in ClientBoundFilterList:
            logger.debug(f"    {packet}")

        logger.debug(f"ServerBound [{len(ServerBoundFilterList)}]:")
        for packet in ServerBoundFilterList:
            logger.debug(f"    {packet}")

    def log_clientbound(*args):
        logger.info(f'\u001b[96mClientBound   {" ".join([str(a) for a in args])}\u001b[0m')

    def log_serverbound(*args):
        logger.info(f'\u001b[95mServerBound   {" ".join([str(a) for a in args])}\u001b[0m')

    def filter_(packet, mode, list_):
        if mode == "blacklist":
            if packet.__class__ in list_:
                return False
            return True

        elif mode == "whitelist":
            if packet.__class__ in list_:
                return True
            return False

    @proxy.ClientBound
    def handler(packet):
        if filter_(packet, cbmode, ClientBoundFilterList):
            log_clientbound(packet) if not limit else log_clientbound(str(packet)[:limit])

    @proxy.ServerBound
    def handler(packet):
        if filter_(packet, sbmode, ServerBoundFilterList):
            log_serverbound(packet) if not limit else log_serverbound(str(packet)[:limit])

    proxy.join()

if __name__ == "__main__":
    main()
