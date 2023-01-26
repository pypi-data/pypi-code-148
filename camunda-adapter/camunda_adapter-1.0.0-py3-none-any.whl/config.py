"""Инструменты конфигурации адаптера."""

from typing import TYPE_CHECKING
from uuid import uuid4

from pydantic.fields import Field
from pydantic.networks import HttpUrl


if TYPE_CHECKING:
    from dataclasses import dataclass  # noqa
else:
    from pydantic.dataclasses import dataclass  # noqa


BPMN_ENGINE_URL = 'BPMN_ENGINE_URL'
BPMN_PROCESS_ID = 'BPMN_PROCESS_ID'
BPMN_LOCK_DURATION = 'BPMN_LOCK_DURATION'
BPMN_ENGINE_REQUEST_TIMEOUT = 'BPMN_ENGINE_REQUEST_TIMEOUT'
BPMN_WORKER_ID = 'BPMN_WORKER_ID'


DEFAULT_REQUEST_TIMEOUT = 30.0  # сек


@dataclass  # pylint: disable=used-before-assignment
class Config:

    """Конфигурация адаптера."""

    engine_url: HttpUrl = Field(
        title='URL движка',
        default='http://127.0.0.1:8080/engine-rest/'
    )
    lock_duration: int = Field(
        title='Продолжительность блокировки задачи при её получении',
        default=1000  # мс
    )
    request_timeout: float = Field(
        title='Таймаут запроса к BPMN',
        default=DEFAULT_REQUEST_TIMEOUT
    )
    worker_id: str = Field(
        title='ID воркера (для блокировки задач)',
        default=f'camunda-adapter-{str(uuid4())}'
    )
