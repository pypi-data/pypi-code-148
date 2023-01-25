import argparse
import asyncio
import signal
import socket

import grpc
from bluerpc.discovery import start_discovery
from bluerpc.rpc import services_pb2_grpc
from bluerpc.service import BlueRPCService
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    NoEncryption,
    PrivateFormat,
    pkcs12,
)


async def serve(bind_addr="[::]:50052", name="unknown", keystore=None) -> None:
    """
    Run the worker and the mDNS task

    Args:
        bind_addr: the gRPC server bind address
        name: the worker name
        keystore: path to a PKCS12 keystore (used for encryption)
    """
    server = grpc.aio.server()
    services_pb2_grpc.add_BlueRPCServicer_to_server(BlueRPCService(name), server)
    encrypted = False

    if keystore is not None:
        try:
            with open(keystore, "rb") as f:
                (
                    private_key,
                    certificate,
                    additional_certificates,
                ) = pkcs12.load_key_and_certificates(f.read(), b"")
            creds = grpc.ssl_server_credentials(
                [
                    (
                        private_key.private_bytes(
                            Encoding.PEM, PrivateFormat.PKCS8, NoEncryption()
                        ),
                        certificate.public_bytes(Encoding.PEM),
                    )
                ],
                additional_certificates[0].public_bytes(Encoding.PEM),
            )
            server.add_secure_port(bind_addr, creds)
            encrypted = True
        except FileNotFoundError:
            print("keystore not found, starting with insecure mode")
            server.add_insecure_port(bind_addr)
    else:
        server.add_insecure_port(bind_addr)

    await server.start()
    print(f"BlueRPC worker running on {bind_addr}")

    await start_discovery(bind_addr, name, encrypted)

    await server.wait_for_termination()


def handler(a, b) -> None:
    """
    Callback for sigint/sigterm, terminates the worker
    """
    exit(0)


def run():
    """
    Parse the arguments and start the worker
    """
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    parser = argparse.ArgumentParser(description="BlueRPC Worker")
    parser.add_argument(
        "--bind_addr",
        type=str,
        help="bind address of the server",
        default="[::]:50052",
        nargs="?",
    )
    parser.add_argument(
        "--name",
        type=str,
        help="name of this worker",
        default=socket.gethostname().split(".")[0].lower(),
        nargs="?",
    )
    parser.add_argument(
        "--keystore", type=str, help="path to the keystore", default=None, nargs="?"
    )
    args = parser.parse_args()

    loop = asyncio.new_event_loop()
    loop.run_until_complete(serve(args.bind_addr, args.name, args.keystore))
