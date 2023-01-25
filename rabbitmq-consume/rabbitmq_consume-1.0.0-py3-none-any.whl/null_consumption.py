"""
Defines the NullConsumption class.
"""

import logging

from pika.spec import BasicProperties


class NullConsumption:
    """
    This implementation of the Consumption Protocol simply log a begin
    and end message to the debug stream.
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
            delivery_tag: The tag identifying the RabbitMQ message.
        """
        self.__delivery_tag = delivery_tag

    def consume(self) -> None:
        """
        Consumes the XML body of a RabbitMQ message.
        """
        logging.debug("BEGIN CONSUMPTION")
        logging.debug("END CONSUMPTION")

    def delivery_tag(self) -> int:
        """
        Returns the tag identifying the RabbitMQ message.
        """
        return self.__delivery_tag
