"""Console script for quantnet_controller."""
import sys
import click
import asyncio

from quantnet_controller.server import QuantnetServer as Quantnet
from quantnet_controller.client.client import QuantnetClient
from quantnet_controller.common.config import Config

STARTUP_FAILURE = 3

STOP = asyncio.Event()

def ask_exit(*args):
    STOP.set()
    
@click.command(help="Quantnet Controller")
@click.option(
    "--mq-broker-host",
    "mq_broker_host",
    type=str,
    default="127.0.0.1",
    help="Reach message queue broker to this host.",
    show_default=True,
)
@click.option(
    "--mq-broker-port",
    "mq_broker_port",
    type=int,
    default=1883,
    help="Reach message queue broker to this port.",
    show_default=True,
)
@click.option(
    "--mode",
    "mode",
    type=str,
    default="server",
    help="Run as QuantNet Server or Client.",
    show_default=True,
)
def main(
        mq_broker_host, 
        mq_broker_port,
        mode,
) -> None:
    run(
        mq_broker_host,
        mq_broker_port,
        mode,
    )
    
    # """Console script for quantnet_controller."""
    # click.echo("Replace this message by putting your code into "
    #            "quantnet_controller.cli.main")
    # click.echo("See click documentation at https://click.palletsprojects.com/")
    #
    # """ parsing command line options """
    #
    #
    # """ loop """
    # loop = asyncio.get_event_loop()
    # loop.add_signal_handler(signal.SIGINT, ask_exit)
    # loop.add_signal_handler(signal.SIGTERM, ask_exit)
    #
    # loop.run_until_complete(Quantnet(args))
    #
    # return 0

def run(
        mq_broker_host: str = "127.0.0.1",
        mq_broker_port: int = 1883,
        mode: str = "server",
) -> None:
    """ config """
    config = Config(
        mq_broker_host = mq_broker_host,
        mq_broker_port = mq_broker_port,
        )
    
    if mode == "server":
        """ create and start quantnet """
        quantnet = Quantnet(config)
        quantnet.run()

        """ exit if failed """
        if not quantnet.started:
            sys.exit(STARTUP_FAILURE)
    elif mode == "client":
        quantclient = QuantnetClient(config)
        quantclient.run()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
