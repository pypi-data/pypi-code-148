"""
Defines the Protocols used by the Worker class
"""

from typing import Protocol

from pika.spec import BasicProperties


class Consumption(Protocol):
    """
    This Protocol is called by a Worker to consume the XML body of a
    RabbitMQ message.
    """

    def __init__(
        self,
        properties: BasicProperties,
        body: bytes,
        delivery_tag: int,
        redelivered: bool,
    ):
        """
        Creates a Consumption instance of the class that will consume
        the body.

        Args:
            properties: The properties of the message.
            body: the XML body of the RabbitMQ message to be consumed
                by the created Consumption instance.
            delivery_tag: The tag identifying the RabbitMQ message.
            redelivered: True if the supplied body has been delivered
                before.
        """

    def consume(self) -> None:
        """
        Consumes the XML body of a RabbitMQ message.
        """

    def delivery_tag(self) -> int:
        """
        Returns the tag identifying the RabbitMQ message.
        """


class ConsumptionManager(Protocol):
    """
    This Proctocol is called by a Worker to manage its Consumption
    instance.
    """

    def create_consumption(
        self,
        properties: BasicProperties,
        body: bytes,
        delivery_tag: int,
        redelivered: bool,
    ) -> Consumption:
        """
        Creates a Consumption instance of the class that will consume
        the body.

        Args:
            properties: The properties of the message.
            body: the XML body of the RabbitMQ message to be consumed
                by the created Consumption instance.
            delivery_tag: The tag identifying the RabbitMQ message.
            redelivered: True if the supplied body has been delivered
                before.
        """

    def destroy_consumption(self, consumption: Consumption) -> None:
        """
        Signals that the supplied Consumption is not longer needed.

        Args:
            consumption: the Consumption no longer needed.
        """
