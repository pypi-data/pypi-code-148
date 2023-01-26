import json
import logging
from typing import (
    Any,
    List,
)

from kafka import KafkaProducer

from kafka_temporal_mapper.common.config import cfg


class KafkaTemporalClient:
    def __init__(self) -> None:
        self.kafka_producer = None
        self.setup_producer()

    def setup_producer(self) -> None:
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=cfg.kafka.bootstrap,
            ssl_check_hostname=False,
            security_protocol="SASL_SSL",
            sasl_plain_username=cfg.kafka.user,
            sasl_plain_password=cfg.kafka.password,
            sasl_mechanism="SCRAM-SHA-512",
            ssl_cafile=cfg.kafka.ca_file,
            api_version=tuple(map(int, cfg.kafka.api_version.split("."))),
        )

    def send(self, dict_msg: dict) -> None:
        str_msg = json.dumps(dict_msg)
        future = self.kafka_producer.send(cfg.kafka.topic, str_msg.encode())
        future.get(timeout=60)

    def notify(self, name: str, args: Any) -> None:
        logging.info(f"workflow {name} notified its execution")
        workflow = {"type": "workflow", "name": name, "args": args}
        self.send(workflow)

    def subscribe(self, target: str, triggers: List[dict]) -> None:
        trigger_names = [t["name"] for t in triggers]
        logging.info(f"workflow: {target} is subscribing to workflows: {trigger_names}")
        mapping = {"type": "mapping", "target": target, "triggers": triggers}
        self.send(mapping)


def run_client() -> None:
    ktc = KafkaTemporalClient()
    ktc.subscribe("GreetingWorkflow", [{"name": "TriggerWorkflow", "args": {"name": "@name"}}])
    ktc.notify("TriggerWorkflow", {"name": "Workflow Team"})


if __name__ == "__main__":
    run_client()
