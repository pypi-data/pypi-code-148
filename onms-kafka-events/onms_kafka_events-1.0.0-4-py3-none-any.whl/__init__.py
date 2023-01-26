# onms-kafka-events.__init__.py
# author: mmahacek@opennms.com

"""
.. include:: ../README.md
"""

import onms_kafka_events.kafka_consumer_events_pb2 as models
import kafka
from kafka.producer.future import FutureRecordMetadata
from enum import Enum


class Severity(Enum):
    INDETERMINATE = 0
    CLEARED = 1
    NORMAL = 2
    WARNING = 3
    MINOR = 4
    MAJOR = 5
    CRITICAL = 6


class KafkaConnection:
    def __init__(self, servers: list, topic: str) -> None:
        self.servers = servers
        self.producer = kafka.KafkaProducer(bootstrap_servers=servers)
        self.topic = topic

    def create_event(
        self,
        uei: str,
        source: str = "kafka-consumer",
        severity: Severity = Severity.INDETERMINATE,
        host: str = None,
        node_id: int = None,
        ip_address: str = None,
        service_name: str = None,
        if_index: int = None,
        description: str = None,
        dist_poller: str = None,
        log_dest: str = None,
        log_content: str = None,
        **parameters,
    ) -> models.Event:
        """Create a `models.Event` object to be used in `send_event()`

        To include paramenters on the event, add them as additional keyword arguments to this method.

        """
        event = models.Event()
        # Process required fields
        event.uei = uei
        event.source = source
        event.severity = severity.value

        # Check if optional fields are included
        if host:
            event.host = host
        if node_id:
            event.node_id = node_id
        if ip_address:
            event.ip_address = ip_address
        if service_name:
            event.service_name = service_name
        if if_index:
            event.if_index = if_index
        if description:
            event.description = description
        if dist_poller:
            event.dist_poller = dist_poller
        if log_dest:
            event.log_dest = log_dest
        if log_content:
            event.log_content = log_content

        # Add all other parameters as custom EventParameters
        for name, value in parameters.items():
            event.parameter.append(models.EventParameter(name=name, value=str(value)))
        return event

    def _on_send_success(record_metadata):
        print(
            f"Topic: {record_metadata.topic} Partition: {record_metadata.partition} Offset: {record_metadata.offset}"
        )

    def _on_send_error(e):
        print("Kafka send error: ", exc_info=e)

    def send_event(self, event: models.Event, timeout=10) -> FutureRecordMetadata:
        """Send event object to Kafka

        Args:
            event (`models.Event`): Use the `create_event()` method to create an event object.
            timeout (int, optional): Number of seconds to wait for Kafka to confirm receipt of the event. Defaults to 10.

        Returns:
            kafka.producer.future.RecordMetadata
        """
        payload = bytes(event.SerializeToString())
        future = (
            self.producer.send(self.topic, payload)
            .add_callback(self._on_send_success)
            .add_errback(self._on_send_error)
        )
        record_metadata = future.get(timeout=timeout)
        return record_metadata
