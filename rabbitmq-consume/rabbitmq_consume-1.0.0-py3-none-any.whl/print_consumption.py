"""
Defines the PrintConsumption class.
"""

import logging
import xml.dom.minidom

from pika.spec import BasicProperties


class PrintConsumption:
    """
    This implementation of the Consumption Protocol simply print the
        XML message.
    """

    def __init__(
        self,
        _: BasicProperties,
        body: bytes,
        delivery_tag: int,
        ___: bool,
    ):
        """
        Creates a Consumption instance of the class that will consume
        the body.

        Args:
            body: the XML body of the RabbitMQ message to be consumed
                by the created Consumption instance.
            delivery_tag: The tag identifying the RabbitMQ message.
        """
        self.__body = body
        self.__delivery_tag = delivery_tag

    def consume(self) -> None:
        """
        Consumes the XML body of a RabbitMQ message.
        """
        logging.info("BEGIN CONSUMPTION")
        logging.info(xml.dom.minidom.parseString(self.__body).toprettyxml(newl=''))
        logging.info("END CONSUMPTION")

    def delivery_tag(self) -> int:
        """
        Returns the tag identifying the RabbitMQ message.
        """
        return self.__delivery_tag
