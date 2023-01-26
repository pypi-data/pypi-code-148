from datetime import datetime
from dataclasses import dataclass


@dataclass
class ContainerRuntimeInfo:
    cpu_count: int
    cpu_architecture: str
    name: str
    server_version: str
    kernel_version: str
    os_type: str
    os: str
    os_version: str


@dataclass
class Image:
    name: str
    tag: str
    image_id: str
    created: datetime
    size_bytes: float


@dataclass
class Port:
    container: str
    host: str


@dataclass
class Container:
    name: str
    id: str
    status: str
    image: str
    command: str
    ports: list[Port]
