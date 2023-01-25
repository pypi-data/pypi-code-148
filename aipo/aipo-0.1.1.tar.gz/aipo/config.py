from dataclasses import dataclass
from typing import Any, Dict, Union

import yaml

from .backends import get_backend_class


@dataclass(frozen=True)
class Config:
    """App configuration."""

    broker_url: str
    broker_params: Dict[str, Any]
    backend_class: str
    default_queue: str = "aipo_default"
    max_concurrent_tasks: int = 100
    serializer_class: str = "api.serializers.JSONSerializer"

    def __init__(self, config: Union[Dict[str, Any], str]):
        if isinstance(config, str):
            config = self._load_from_file(config)
        self._validate(config)
        super().__init__(**config)

    def _load_from_file(self, path: str) -> Dict[str, Any]:
        with open(path) as f:
            return yaml.safe_load(f)

    def _validate(self, config: Dict[str, Any]) -> None:
        if not config.get("broker_url"):
            raise ValueError("broker_url is required")

        mct = config.get("max_concurrent_tasks")
        if mct and mct < 1:
            raise ValueError("max_concurrent_tasks must be greater than 0")

        if not config.get("broker_class"):
            config["broker_class"] = get_backend_class(config["broker_url"])

        if not config.get("broker_params"):
            config["broker_params"] = {}

        self._parse_broker_url(config)

    def _parse_broker_url(self, config: Dict[str, Any]) -> None:
        config["broker_params"].update(
            {
                "hostname": config["broker_url"].split("//")[1].split(":")[0],
                "port": int(
                    config["broker_url"].split("//")[1].split(":")[1].split("/")[0]
                ),
            }
        )

        if config["broker_url"].startswith("redis://"):
            if "/" in config["broker_url"].split("//")[1]:
                db = config["broker_url"].split("//")[1].split("/")[1]
                config["broker_params"].update({"db": db})
