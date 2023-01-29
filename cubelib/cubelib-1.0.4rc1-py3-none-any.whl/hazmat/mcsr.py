from cubelib.hazmat.mcct import StatusRetriver
import argparse
import logging
from .util import CustomFormatter

version = "0.1.0"

def main():
    parser = argparse.ArgumentParser(description=F"Minecraft Server Status Retriever v{version}")
    parser.add_argument("host", help="Minecraft server in addr:port format like [localhost:25565]", metavar="host")
    parser.add_argument("-v", action="store_true", help="If passed, show sent and recieved packets")
    parser.add_argument("-p", type=int, help="Protocol version, field sent in Handshake packet", default="2147483647", metavar="proto_ver")
    args = parser.parse_args()

    logger = logging.getLogger("")
    logger.setLevel(logging.INFO)
    stdout_handler = logging.StreamHandler()
    stdout_handler.setLevel(logging.DEBUG)
    stdout_handler.setFormatter(CustomFormatter('[%(asctime)s] [%(levelname)s] %(name)s:  %(message)s'))
    logger.addHandler(stdout_handler)
    
    def host2ap(addr: str):
        x = addr.split(":")
        if len(x) == 1:
            return x[0], 25565
        return x[-2], int(x[-1])

    logger.info(F"Minecraft Server Status Retriever v{version}")
    logger.info(F"Retrieving status of {args.host}")
    try:
        status, ping = StatusRetriver(*host2ap(args.host), args.p, args.v).retrieve()
    except TimeoutError:
        logger.critical(F"Failed to retrieve server status!")
        return
    logger.info(F"Ping: {ping}ms")
    logger.info(F"{status}")
    