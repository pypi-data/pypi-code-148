from __future__ import annotations

from dataclasses import dataclass
import logging
import os
import re
from typing import Optional

import dacite
from temporallib.connection.connection import Options
import yaml


@dataclass
class MapperConfig:
    sensors: list


@dataclass
class KafkaConfig:
    bootstrap: str
    user: str
    password: str
    topic: str
    consumer_group: str
    ca: str
    ca_file: str = "/tmp/temporal-kafka-ca.crt"
    api_version: str = "2.5.0"

    def save_ca(self) -> None:
        with open(self.ca_file, "w") as ca:
            ca.write(self.ca)


@dataclass
class LoggerConfig:
    level: str = "INFO"
    file: Optional[str] = None


@dataclass
class Config:
    kafka: KafkaConfig
    temporal: Options
    mapper: MapperConfig = MapperConfig(sensors=["Temporal"])
    logger: LoggerConfig = LoggerConfig()


def load_config() -> Config:
    """Loads the configuration from the file specified in CONFIG_PATH env"""

    def_path = f"{os.path.dirname(__file__)}/config.yaml"
    config_path = os.getenv("CONFIG_PATH")

    if config_path is None and os.path.isfile(def_path):
        config_path = def_path

    if config_path is None:
        raise ConfigException("CONFIG_PATH environment variable not set")

    try:
        setup_env_yaml()
        with open(config_path, "r") as f:
            cfg_yml = yaml.load(f, Loader=yaml.FullLoader)
        conf = dacite.from_dict(data_class=Config, data=cfg_yml)
    except FileNotFoundError:
        raise ConfigException(f"Config file ({config_path}) does not exist.")
    except yaml.YAMLError as e:
        raise ConfigException(f"Config file ({config_path}) has incorrect yaml format: {e}")
    except dacite.DaciteError as e:
        raise ConfigException(f"Config ({config_path}) parsing error: {e}.")

    return conf


def setup_env_yaml() -> None:
    """Sets up the yaml parser to replace references to environment variables with their value"""

    path_matcher = re.compile(r"\$\{([^}^{]+)\}")

    def path_constructor(loader, node):
        """Extract the matched value, expand env variable, and replace the match"""

        value = node.value
        match = path_matcher.match(value)
        env_var = match.group()[2:-1]
        return os.environ.get(env_var) + value[match.end() :]

    yaml.add_implicit_resolver("!path", path_matcher)
    yaml.add_constructor("!path", path_constructor)


class ConfigException(Exception):
    """Exception raised when something wrong goes when loading the configuration file."""


cfg = load_config()
cfg.kafka.save_ca()
logging.basicConfig(
    datefmt="%Y-%m-%d %H:%M:%S",
    format="%(asctime)s %(levelname)s:\t%(message)s",
    level=cfg.logger.level.upper(),
    filename=cfg.logger.file,
)
