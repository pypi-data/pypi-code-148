"""
Defines the Push class.
"""

from typing import Optional

import logging

import pika
from pika.adapters.blocking_connection import BlockingChannel

# from pika.spec import BasicProperties


class Pusher:
    """
    This class pushes a raw XML message onto a RabbitMQ queue.
    """

    def __init__(
        self,
        connection_parameters: pika.connection.Parameters,
        queue: str,
        durable: bool = True,
    ):
        """
        Create a new instance of the Pusher class, passing in the AMQP
        URL used to connect to RabbitMQ.

        Args:
            connection_parameters: The parameters to use to connect
                to the server.
            queue: The rabbitMQ queue to which this client should push.
            durable: true if pushed messages are durable rather than
                transient.
        """
        self._connection: Optional[pika.BlockingConnection] = None
        self._channel: Optional[BlockingChannel] = None

        self._connection_parameters = connection_parameters
        self._queue = queue
        self._durable = durable
        if self._durable:
            self._delivery_mode: int = pika.spec.PERSISTENT_DELIVERY_MODE
        else:
            self._delivery_mode = pika.spec.TRANSIENT_DELIVERY_MODE

    def close_connection(self) -> None:
        """
        Closes the connection, if still open.
        """
        if None is not self._connection:
            self._connection.close()

    def close_channel(self) -> None:
        """
        Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.
        """
        if None is self._channel:
            logging.warning("Channel can not be closed as it does not exist")
            return
        logging.info("Closing the channel")
        self._channel.close()

    def connect(self) -> pika.BlockingConnection:
        """
        This method connects to RabbitMQ, returning the connection
        handle. When the connection is established, the
        channel is opened.

        Return:
            pika.SelectConnection
        """
        logging.info("Connecting to %s", self._connection_parameters)
        self._connection = pika.BlockingConnection(self._connection_parameters)
        self.open_channel()
        if None is self._channel:
            logging.warning("Channel failed to open")
        return self._connection

    def open_channel(self) -> None:
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.
        """
        if None is self._connection:
            logging.warning("Channel was not opennd as Connection does not exist")
            return
        logging.info("Creating a new channel")
        self._channel = self._connection.channel()
        if None is self._channel:
            logging.warning("Channel failed to open")
            return
        self._channel.queue_declare(queue=self._queue, durable=self._durable)

    def push(self, message: str) -> None:
        """
        Pushed the supplied XML message to this Object's RabbitMQ queue,
        """
        if None is self._channel:
            logging.warning("Message was not published as Channel does not exist")
            return
        self._channel.basic_publish(
            exchange="",
            routing_key=self._queue,
            body=message,
            properties=pika.BasicProperties(
                content_type="text/xml",
                delivery_mode=self._delivery_mode,
            ),
        )
