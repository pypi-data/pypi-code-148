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
    parser.add_argument("-l", help="Proxy listen addr [localhost:25565]", default="127.0.0.1:25565", metavar="addr")
    parser.add_argument("-u", help="Proxy upstream server addr [localhost:25575]", default="127.0.0.1:25575", metavar="addr")
    args = parser.parse_args()
    
    if args.c:
        yaml = YAML(typ="safe")
        conf = yaml.load(args.c)
    else:
        conf = {"mode": "blacklist"}

    def addr_str2tuple(addr: str):
        s = addr.split(":")
        return (s[0], int(s[1]))

    logger = logging.getLogger("")
    logger.setLevel(logging.DEBUG if args.v else logging.INFO)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter('[%(asctime)s] [%(levelname)s] %(name)s:  %(message)s'))
    logger.addHandler(stdout_handler)

    proxy = MCRewriteProxy(addr_str2tuple(args.l), addr_str2tuple(args.u), logging.INFO if args.v else logging.ERROR)

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
                    logger.warn(f'Failed to resolve filter packet {proxy.PROTOCOL.__name__}.{".".join(attrs)}')
                    break
            return obj
        
        ClientBoundFilterList = [find_ap_by_path(proto, "ClientBound.Play." + packet) for packet in conf["ClientBound"]] if "ClientBound" in conf else []
        ServerBoundFilterList = [find_ap_by_path(proto, "ServerBound.Play." + packet) for packet in conf["ServerBound"]] if "ServerBound" in conf else []

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
        if filter_(packet, conf["mode"], ClientBoundFilterList):
            log_clientbound(packet)

    @proxy.ServerBound
    def handler(packet):
        if filter_(packet, conf["mode"], ServerBoundFilterList):
            log_serverbound(packet)                

    proxy.join()

if __name__ == "__main__":
    main()
