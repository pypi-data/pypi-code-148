"""
Defines the NullConsumption class.
"""

import logging

from pika.spec import BasicProperties


class NullConsumption:
    """
    This implementation of the Consumption Protocol simply print a begin
    and end message.
    """

    def __init__(
        self,
        _: BasicProperties,
        __: bytes,
        delivery_tag: int,
        ___: bool,
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
        self.__delivery_tag = delivery_tag

    def consume(self) -> None:
        """
        Consumes the XML body of a RabbitMQ message.
        """
        logging.info("BEGIN CONSUMPTION")
        logging.info("END CONSUMPTION")

    def delivery_tag(self) -> int:
        """
        Returns the tag identifying the RabbitMQ message.
        """
        return self.__delivery_tag
