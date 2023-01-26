# event_generator.py
# author: mmahacek@opennms.com

import kafka_consumer_events_pb2
import kafka
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
        uei: str = "uei.opennms.org/internal/kafka/consumer/unknown",
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
    ) -> kafka_consumer_events_pb2.Event:
        event = kafka_consumer_events_pb2.Event()
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
            event.parameter.append(
                kafka_consumer_events_pb2.EventParameter(name=name, value=str(value))
            )
        return event

    def _on_send_success(record_metadata):
        print(
            f"Topic: {record_metadata.topic} Partition: {record_metadata.partition} Offset: {record_metadata.offset}"
        )

    def _on_send_error(e):
        print("Kafka send error: ", exc_info=e)

    def send_event(
        self, event: kafka_consumer_events_pb2.Event, timeout=10
    ) -> kafka.producer.future.RecordMetadata:
        payload = bytes(event.SerializeToString())
        # self.producer.send(self.topic, payload)

        future = (
            self.producer.send(self.topic, payload)
            .add_callback(self._on_send_success)
            .add_errback(self._on_send_error)
        )
        record_metadata = future.get(timeout=timeout)
        return record_metadata


if __name__ == "__main__":
    # Establish a connection to the Kafka broker
    my_producer = KafkaConnection(
        servers=["broker1:9092", "broker2:9092"],
        topic="opennms-kafka-events",  # This should match the topic configured for the Kafka Consumer feature
    )

    # Send a bare bones event based on the foreign source information

    my_event_fid = my_producer.create_event(
        uei="uei.opennms.org/custom/event/name",
        severity=Severity.NORMAL,
        _foreignSource="requisitionName",
        _foreignId="12345",
    )
    message = my_producer.send_event(my_event_fid)
    print(
        message
    )  # The send_event method returns a RecordMetadata object with information about where the message was sent

    # Send a bare bones event based on the node's database ID

    my_event_db = my_producer.create_event(
        uei="uei.opennms.org/custom/event/name",
        severity=Severity["MINOR"],  # If assigning a severity based on a string value
        node_id=101,
    )
    my_producer.send_event(
        my_event_db, timeout=30
    )  # By default, the send_event method will wait 10 seconds for a response from the Kafka broker.
    # You can change this timeout by passing a different value to the timeout parameter.

    # Send send an event related to a specific IP interface

    my_event_ip = my_producer.create_event(
        uei="uei.opennms.org/custom/event/interfaceIssue",
        severity=Severity(3),  # If assigning a severity based on the enum value
        node_id=19,
        ip_address="192.168.42.69",
        description="Interface is wonky",
        wonky_factor=11,
    )
    my_producer.send_event(my_event_ip)

    # Send send an event related to a specific SNMP interface

    my_event_snmp = my_producer.create_event(
        uei="uei.opennms.org/custom/event/interfaceIssueUp",
        severity=Severity.CLEARED,  # If assigning a severity based on the enum value
        node_id=19,
        # if_index=3,
        wonky_factor=0,
        description="Interface id %if_index% has a wonky factor of %parm[wonky_factor]%",
    )
    my_producer.send_event(my_event_snmp)

    # Send send an event related to a specific service

    urgency = "CRITICAL"
    my_event_srv = my_producer.create_event(
        uei="uei.opennms.org/custom/event/dbIssue",
        severity=Severity[urgency],  # Passing the severity as a string variable
        node_id=19,
        ip_address="192.168.42.69",
        service_name="Postgres",
        description="Table has flipped",
        table="important_items",
    )
    my_producer.send_event(my_event_srv)

    # Trigger a Passive Status Keeper event

    my_event_psk = my_producer.create_event(
        uei="uei.opennms.org/services/passiveServiceStatus",  # Passive Status Keeper expects this specific UEI
        severity=Severity.MAJOR,
        node_id=19,
        passiveNodeLabel="core_router",  # Must match the label of the node in the database
        passiveIpAddr="192.168.42.1",  # Must match the IP address of the passive service name
        passiveServiceName="PSK-pollerd-name",  # Must match a PassiveServiceStatus poller named assigned to the node
        passiveStatus="Down",  # Either "Up" or "Down", case-sensitive
        passiveReasonCode=1337,  # Optional reason code
    )
    my_producer.send_event(my_event_psk)
