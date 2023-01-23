"""Defines the Worker class used by the Consumer class"""

import threading
import traceback

from pika.spec import BasicProperties, Basic

from .consumption import ConsumptionManager


class Worker(threading.Thread):
    """
    This class manages the execution of a message for the Consumer class.
    """

    def __init__(
        self,
        consumption_manager: ConsumptionManager,
        deliver: Basic.Deliver,
        properties: BasicProperties,
        body: bytes,
    ):
        """
        Creates an instance of this class.

        Args:
            consumption_manager: The ConsumerManager that is managing
                this object.
            deliver: The detail about delivery of the message.
            properties: The properties of the message.
            body: The body of the message.
        """
        threading.Thread.__init__(self)
        self.__consumption_manager = consumption_manager
        self.__consumption_instance = None
        if None is deliver or None is deliver.delivery_tag:
            raise ValueError("Incomplete or missing Deliver object")
        self.__consumption_instance = self.__consumption_manager.create_consumption(
            properties, body, deliver.delivery_tag, deliver.redelivered
        )

    def run(self):
        if None is self.__consumption_instance:
            return
        try:
            self.__consumption_instance.consume()
        except Exception:  # pylint: disable=broad-except
            traceback.print_exc()
        self.__consumption_manager.destroy_consumption(self.__consumption_instance)
