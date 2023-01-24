"""
Defines the Consumer class.

Based on http://pika.readthedocs.org/en/latest/examples/asynchronous_consumer_example.html

Changes include, but not limited to, removal of Exchange binding, doing
the consumption in a separate thread and adding wait and time to live
timeouts.
"""

from typing import Callable, Optional, Type, Union

import functools
from importlib.metadata import entry_points
import logging
import threading

import pika
from pika.channel import Channel
from pika.adapters.base_connection import BaseConnection

# from pika.adapters.select_connection import IOLoop
from pika.spec import BasicProperties, Basic

from .consumption import Consumption
from .worker import Worker


def __select_consumption_type(name) -> Type[Consumption]:
    """
    Returns the selected drop.Dropper class object.
    """
    consumptions = entry_points(group="rmq_consume.consumption")
    known_values = []
    logging.debug("Begin known Consumption Types:")
    for entry in consumptions:
        if entry.value not in known_values:
            logging.debug("    %s", entry)
            known_values.append(entry.value)
    logging.debug("End known Consumption Types:")
    for entry in consumptions:
        if name == entry.value:
            return entry.load()
    raise ValueError(f'No known Consumption implementation named "{name}"')


class Consumer:  # pylint: disable=too-many-instance-attributes,too-many-public-methods
    """This is an example consumer that will handle unexpected interactions
    with RabbitMQ such as channel and connection closures.

    If RabbitMQ closes the connection, this class will stop and indicate
    that reconnection is necessary. You should look at the output, as
    there are limited reasons why the connection may be closed, which
    usually are tied to permission related issues or socket timeouts.

    If the channel is closed, it will indicate a problem with one of the
    commands that were issued and that should surface in the output as well.

    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        connection_parameters: pika.connection.Parameters,
        queue: str,
        target: str,
        prefetch=1,
        restart: int = 0,
        durable: bool = True,
        live_time: float = 0.0,
        wait_time: float = 0.0,
    ):
        """Create a new instance of the Consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.

        Args:
            connection_parameters: The parameters to use to connect
                to the server.
            queue: The rabbitMQ queue which this client should consume.
            target: The name of the Consumption plugin to use.
            prefetch: The number of workers, and this the number of
                messages to prefetch.
            restart: The number of seconds to wait before attempting
                to reconnect after a lost connection. Zero or less
                means no reconnect will be attempted.
            durable: true if the specified queue is durable rather
                than transient.
            wait_time: The number of seconds that this client should
                wait with no message before it gracefully exits.
        """
        self.should_reconnect = False
        self.was_consuming = False

        self._connection: Optional[BaseConnection] = None
        self._channel: Optional[Channel] = None
        self._closing = False
        self._consumer_tag: Optional[str] = None
        # self._url = amqp_url # replaced by client supplied parameters
        self._consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1

        # Exdended attributes
        self._connection_parameters = connection_parameters
        self._queue = queue
        self._target = target
        self._restart = restart
        self._durable = durable
        self._active = 0
        self._wait_time = wait_time
        self._prefetch = prefetch

        if live_time > 0:
            self._live = threading.Timer(live_time, self.__expired_listening)
            self._live.start()
        self._wait: Optional[threading.Timer] = None
        self._listening = True

    def connect(self) -> pika.SelectConnection:
        """This method connects to RabbitMQ, returning the connection
        handle. When the connection is established, the
        on_connection_open method will be invoked by pika.

        Return:
            pika.SelectConnection
        """
        logging.info("Connecting to %s", self._connection_parameters)
        return pika.SelectConnection(
            parameters=self._connection_parameters,
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )

    def close_connection(self) -> None:
        """Closes the connection, if still open."""
        self._consuming = False
        if None is self._connection:
            logging.warning("Connection can not be closed as it does not exist")
            return
        if self._connection.is_closing or self._connection.is_closed:
            logging.info("Connection is closing or already closed")
        else:
            logging.info("Closing connection")
            self._connection.close()

    def on_connection_open(  # pylint: disable=unsubscriptable-object
        self, _unused_connection
    ) -> None:
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        Args:
            _unused_connection: The connection
        """
        logging.info("Connection opened")
        self.open_channel()

    def on_connection_open_error(  # pylint: disable=unsubscriptable-object
        self, _unused_connection, err: Union[str, Exception]
    ) -> None:
        """This method is called by pika if the connection to RabbitMQ
        can't be established.

        Args:
            _unused_connection: The connection
            err: The error
        """
        logging.error("Connection open failed: %s", err)
        self.reconnect()

    def on_connection_closed(
        self, _unused_connection: pika.connection.Connection, reason: Exception
    ) -> None:
        """This method is invoked by pika when the connection to RabbitMQ
        is closed unexpectedly. Since it is unexpected, we will
        reconnect to RabbitMQ if it disconnects.

        Args:
            _unused_connection: The closed connection object
            reason: exception representing reason for loss of
                connection.
        """
        self._channel = None
        if self._closing or 0 >= self._restart:
            if None is self._connection:
                logging.warning("Connection was not closed as it does not exist")
                return
            if None is self._connection.ioloop:
                logging.warning("Connection was not closed as ioloop does not exist")
                return
            self._connection.ioloop.stop()
        else:
            logging.warning("Connection closed, reconnect necessary: %s", reason)
            self.reconnect()

    def reconnect(self) -> None:
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.
        """
        if not self._closing:
            self.should_reconnect = True
            self.stop()

    def open_channel(self) -> None:
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.
        """
        if None is self._connection:
            logging.warning("Channel was not openned as Connection does not exist")
            return
        logging.info("Creating a new channel")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel: Channel) -> None:
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll set up the queue
        exchange steps).

        Args:
            channel: The channel object
        """
        logging.info("Channel opened")
        self._channel = channel
        self.add_on_channel_close_callback()
        self.setup_queue(self._queue)

    def add_on_channel_close_callback(self) -> None:
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.
        """
        if None is self._channel:
            logging.warning("Could not add Close callback as Channel does not exist")
            return
        logging.info("Adding channel close callback")
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel: Channel, reason: Exception) -> None:
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        Args:
            channel: The closed channel.
            reason: why the channel was closed.
        """
        logging.warning("Channel %i was closed: %s", channel, reason)
        self.close_connection()

    def setup_queue(self, queue_name: str) -> None:
        """Setup the queue on RabbitMQ by invoking the Queue.Declare RPC
        command. When it is complete, the on_queue_declareok method will
        be invoked by pika.

        Args:
            queue_name: The name of the queue to declare.
        """
        if None is self._channel:
            logging.warning("Could not set up Queue as Channel does not exist")
            return
        logging.info("Declaring queue %s", queue_name)
        callback = functools.partial(self.on_queue_declareok, userdata=queue_name)
        self._channel.queue_declare(
            queue=queue_name, callback=callback, durable=self._durable
        )

    def on_queue_declareok(
        self, _unused_frame: pika.frame.Method, userdata: str
    ) -> None:
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we start the consumption
        of the queue.

        Args:
            _unused_frame: The Queue.DeclareOk frame
            userdata: Extra user data (queue name)
        """
        logging.info("Starting consumption from queue %s", userdata)
        self.start_consuming()

    def start_consuming(self) -> None:
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.
        """
        if None is self._channel:
            logging.warning("Could not start consumption as Channel does not exist")
            return
        logging.info("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self._queue, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self) -> None:
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.
        """
        if None is self._channel:
            logging.warning("Could not add Cancel callback as Channel does not exist")
            return
        logging.info("Adding consumer cancellation callback")
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame: pika.frame.Method) -> None:
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        Args:
            method_frame: The Basic.Cancel frame
        """
        logging.info("Consumer was cancelled remotely, shutting down: %r", method_frame)
        if self._channel:
            self._channel.close()

    def on_message(
        self,
        _unused_channel: Channel,
        basic_deliver: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ) -> None:
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        Args:
            _unused_channel: The channel object
            basic_deliver: The detail about delivery of the message.
            properties: The properties of the message
            body: The body of the message
        """
        logging.info(
            "Received message # %s from %s: %s",
            basic_deliver.delivery_tag,
            properties.app_id,
            body,
        )
        self._active += 1
        if None is not self._wait:
            self._wait.cancel()
            self._wait = None
        runner = Worker(self, basic_deliver, properties, body)
        runner.start()

    def acknowledge_message(self, delivery_tag: int) -> None:
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        Args:
            delivery_tag: The delivery tag from the Basic.Deliver frame
        """
        if None is self._channel:
            logging.warning("Could not ACK message as Channel does not exist")
            return
        logging.info("Acknowledging message %s", delivery_tag)
        self._channel.basic_ack(delivery_tag)
        self._active -= 1
        if 0 == self._active:
            self.__start_waiting()
        if not self._listening:
            self._prefetch -= 1
            self._channel.basic_qos(prefetch_count=self._prefetch)
            if 0 == self._prefetch:
                logging.info("Stopping as there no Workers and no longer listening")
                callback = functools.partial(self.stop, internal_stop=True)
                self.__add_timeout(0, callback)
            else:
                logging.info(
                    "Worker count changed to %i as no longer listening", self._prefetch
                )

    def stop_consuming(self) -> None:
        """Tell RabbitMQ that you would like to stop consuming by sending
        the Basic.Cancel RPC command.
        """
        if self._channel and self._consumer_tag:
            logging.info("Sending a Basic.Cancel RPC command to RabbitMQ")
            callback = functools.partial(self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, callback)

    def on_cancelok(self, _unused_frame: pika.frame.Method, userdata: str) -> None:
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        Args:
            _unused_frame: The Basic.CancelOk frame
            userdata: Extra user data (consumer tag)
        """
        self._consuming = False
        logging.info(
            "RabbitMQ acknowledged the cancellation of the consumer: %s", userdata
        )
        self.close_channel()

    def close_channel(self) -> None:
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.
        """
        if None is self._channel:
            logging.warning("Channel can not be closed as it does not exist")
            return
        logging.info("Closing the channel")
        self._channel.close()

    def run(self) -> None:
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """
        self._connection = self.connect()
        if None is self._connection:
            logging.warning("Connection failed to be established")
            return
        if None is self._connection.ioloop:
            logging.warning("IOLoop was not started as it does not exist")
            return
        self._connection.ioloop.start()

    def stop(self, internal_stop: bool = False) -> None:
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        Args:
            internal_stop: True if the request
        """
        if not self._closing:
            self._closing = True
            logging.info("Stopping")
            if self._consuming:
                self.stop_consuming()
                if not internal_stop:
                    if None is self._connection:
                        logging.warning(
                            "Can not restart IOLoop as there is no Connection"
                        )
                        return
                    if None is self._connection.ioloop:
                        logging.warning("IOLoop was not started as it does not exist")
                        return
                    self._connection.ioloop.start()
            else:
                if None is self._connection:
                    logging.warning("Can not restart IOLoop as there is no Connection")
                    return
                if None is self._connection.ioloop:
                    logging.warning("IOLoop was not started as it does not exist")
                    return
                self._connection.ioloop.stop()
            logging.info("Stopped")

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
        consumption_type = __select_consumption_type(self._target)
        return consumption_type(properties, body, delivery_tag, redelivered)

    def destroy_consumption(self, consumption: Consumption) -> None:
        """
        Signals that the supplied Consumption is not longer needed.

        Args:
            consumption: the Consumption no longer needed.
        """
        callback = functools.partial(
            self.acknowledge_message, delivery_tag=consumption.delivery_tag()
        )
        self.__add_timeout(0, callback)

    def __add_timeout(self, delay: float, callback: Callable[[], None]) -> None:
        """
        Put the callback call on this object's callback queue.

        Args:
            delay: who long to wait before executing the callback.
            callback: The callback to be added.
        """
        if None is self._connection:
            logging.warning("Can not queue callback as there is no Connection")
            return
        if None is self._connection.ioloop:
            logging.warning("Can not queue callback as there is no IOLoop")
            return
        self._connection.ioloop.call_later(delay, callback)

    def __start_waiting(self) -> None:
        """Starts the wait time when this client has no message."""
        if self._wait_time > 0:
            self._wait = threading.Timer(self._wait_time, self.__expired_wait)
            self._wait.start()
        else:
            self._wait = None

    def __expired_wait(self) -> None:
        """Put the stop_waiting call on this object's callback queue."""
        self.__add_timeout(0, self.__stop_waiting)

    def __stop_waiting(self) -> None:
        """This method is called to gracefully shut down the connection when
        it's waiting time has been exceeded and no message received.
        """
        if 0 != self._active:
            return
        if None is self._channel:
            logging.warning(
                "Wist time expired by could not stop as Channel does not exist"
            )
            return
        self._channel.basic_qos(prefetch_count=0)
        logging.info(
            "Stopping as the wait time has been exceeded and no message received"
        )
        callback = functools.partial(self.stop, internal_stop=True)
        self.__add_timeout(0, callback)

    def __expired_listening(self):
        self.__add_timeout(0, self.__stop_listening)

    def __stop_listening(self):
        """This method is called to gracefully shut down the connection when
        the 'live_time' parameters has been exceeded.
        """
        changed = False
        if self._prefetch != self._active:
            # Reduce the pre-fetch to the number of currently active
            # connections.
            self._prefetch = self._active
            changed = True
            self._channel.basic_qos(prefetch_count=self._prefetch)
        if 0 == self._prefetch:
            logging.info("Stopping as there no Workers and no longer listening")
            callback = functools.partial(self.stop, internal_stop=True)
            self.__add_timeout(0, callback)
        else:
            self._listening = False
            if changed:
                logging.info(
                    "Worker count changed to %s as no longer listening",
                    str(self._prefetch),
                )
