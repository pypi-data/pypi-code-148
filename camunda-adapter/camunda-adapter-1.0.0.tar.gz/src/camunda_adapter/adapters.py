"""Модуль адаптера к платформе Camunda."""

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Optional
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse
from uuid import uuid4
import logging

import requests

from .config import Config
from .const import PATH_SEP
from .domain import model


logger = logging.getLogger(__name__)


TopicHandler = Callable[[model.ExternalTask, 'Adapter'], Any]


class AbstractTopicHandlerRegistry(ABC):

    """Абстрактный реестр обработчиков внешних задач."""

    _registry: Dict[model.Topic, TopicHandler]

    def __init__(self):
        self._registry = {}

    @abstractmethod
    def register(self, topic: model.Topic, handler: TopicHandler):
        """Зарегистрировать обработчик."""

    @abstractmethod
    def replace(self, topic: model.Topic, handler: TopicHandler):
        """Заменить обработчик."""

    @abstractmethod
    def get(self, topic: model.Topic) -> TopicHandler:
        """Получить обработчик по топику."""


class TopicHandlerRegistry(AbstractTopicHandlerRegistry):

    """Реестр обработчиков внешних задач."""

    def register(self, topic: model.Topic, handler: TopicHandler):
        if topic in self._registry:
            raise ValueError(f'Обработчик "{topic}" уже зарегистрирован')
        self._registry[topic] = handler
        logger.info('Обработчик "%s" зарегистрирован', topic)

    def replace(self, topic: model.Topic, handler: TopicHandler):
        if topic not in self._registry:
            logger.warning('Обработчик "%s" не был зарегистрирован', topic)
        self._registry[topic] = handler
        logger.info('Обработчик "%s" зарегистрирован', topic)

    def get(self, topic: model.Topic) -> TopicHandler:
        handler = self._registry.get(topic)
        if handler is None:
            raise ValueError(f'Обработчик "{topic}" не был зарегистрирован')
        return handler


class Session(requests.Session):

    """Сессия, определяющая параметры запросов к Camunda."""

    _config: Config

    def __init__(
        self,
        config: Config,
        *args, **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._config = config

    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', self._config.request_timeout)
        return super().request(*args, **kwargs)


class Adapter:

    """Адаптер к движку Camunda."""

    _config: Config
    _session: Session

    def __init__(self, config: Config):
        self._config = config
        self._session = Session(config=self._config)
        self._topic_registry = TopicHandlerRegistry()

        logger.info('Camunda adapter worker_id: %s', self._config.worker_id)

    # ########################################################################
    # Deployments
    # ########################################################################
    def get_deployments(
        self
    ) -> Iterable[model.Deployment]:
        """Получить все развертывания."""

        response = self._session.get(
            self._build_url('/deployment')
        )
        response.raise_for_status()
        for data in response.json():
            yield model.Deployment(**data)

    def create_deployment(self, name: str, diagram_file: Path):
        """Создать развертывание.

        Загружает файл BPMN-диаграммы и создает развертывание с именем name.
        """

        with diagram_file.open('r') as fd:
            response = self._session.post(
                self._build_url(
                    '/deployment/create'
                ),
                files={
                    'data': fd
                },
                data={
                    'deployment-name': name,
                    'deploy-changed-only': 'true'
                }
            )
            response.raise_for_status()
            return model.Deployment(**response.json())

    def rm_deployment(
        self,
        deployment: model.Deployment,
        cascade=False
    ):
        """Удалить развертывание."""

        response = self._session.delete(
            self._build_url(
                '/deployment/{id}', cascade=cascade
            ).format(id=deployment.id)
        )
        response.raise_for_status()

    # ########################################################################
    # Definitions
    # ########################################################################
    def get_definitions(
        self
    ) -> Iterable[model.Definition]:
        """Получить все определения процессов."""

        response = self._session.get(
            self._build_url('/process-definition/')
        )
        response.raise_for_status()
        for data in response.json():
            yield model.Definition(**data)

    def get_definition_by_key(
        self,
        key: str
    ) -> model.Definition:
        """Получить определение процесса по его ключу."""

        for definition in self.get_definitions():
            if definition.key == key:
                return definition
        else:
            raise ValueError(f'Процесс "{key}" не найден')

    def rm_definition(
        self,
        process_definition: model.Definition,
        cascade=True,
        skip_custom_listeners=False,
        skip_io_mappings=False
    ):
        """Удалить определение процесса."""

        response = self._session.delete(
            self._build_url(
                '/process-definition/key/{key}',
                cascade=cascade,
                skipCustomListeners=skip_custom_listeners,
                skipIoMappings=skip_io_mappings
            ).format(key=process_definition.key)
        )
        response.raise_for_status()

    # ########################################################################
    # Processes
    # ########################################################################
    def get_processes(self):
        """Получить все экземпляры процессов."""

        response = self._session.get(
            self._build_url('/process-instance')
        )
        response.raise_for_status()
        for data in response.json():
            yield model.Process(**data)

    def start_process(
        self,
        process_definition: model.Definition,
        business_key=None,
        **variables
    ):
        """Запуск процесса.

        Может быть запущен процесс, имеющий StartEvent в качестве точки входа.
        """

        payload = {
            'businessKey': business_key or str(uuid4()),
            'variables': {
                name: {
                    'value': value,
                    'type': model.TYPE_MAP[type(value)]
                } for name, value in variables.items()
            }
        }

        response = self._session.post(
            self._build_url(
                '/process-definition/key/{key}/start'
            ).format(key=process_definition.key),
            json=payload
        )
        response.raise_for_status()
        return model.Process(**response.json())

    # ########################################################################
    # Messages
    # ########################################################################
    def message(
        self, message: model.Message
    ):
        """Передача сообщения процессу с коррелирующим message.businessKey."""

        response = self._session.post(
            self._build_url(
                '/message'
            ),
            json=message.dict()
        )
        response.raise_for_status()
        for data in response.json():
            yield model.MessageResult(**data)

    # ########################################################################
    # External tasks
    # ########################################################################
    def get_external_tasks_topics(self):
        """Получить все топики внешних задач."""

        response = self._session.get(
            self._build_url('/external-task/topic-names')
        )
        for topic_name in response.json():
            yield model.Topic(name=topic_name)

    def get_external_tasks(
        self,
        definition: Optional[model.Definition] = None
    ) -> Iterable[model.ExternalTask]:
        """Запрос списка внешних задач.

        Если указан definition, отдает список задач конкретного типа процессов.
        """

        query_params = {}
        if definition is not None:
            query_params['processDefinitionId'] = definition.id

        response = self._session.get(
            self._build_url('/external-task', **query_params)
        )
        response.raise_for_status()

        logger.info(
            'Получено %s внешних задач (definition=%s)',
            len(response.json()), definition.name if definition else definition
        )

        for data in response.json():
            logger.debug(data)
            yield model.ExternalTask(**data)

    def fetch_and_lock_external_tasks(
        self,
        *topics: model.Topic,
        max_tasks: int = 10,
    ) -> Iterable[model.ExternalTask]:
        """Блокировка и получение списка внешних задач по топикам.

        Задачи, заблокированые ранее, не отдаются.

        max_tasks - ограничение по одновременному количеству задач.
        """

        if not topics:
            yield from ()
            return

        response = self._session.post(
            self._build_url(
                '/external-task/fetchAndLock'
            ),
            json={
                'workerId': self._config.worker_id,
                'maxTasks': max_tasks,
                'usePriority': True,
                'topics': [
                    {
                        'topicName': topic.name,
                        'lockDuration': self._config.lock_duration
                    }
                    for topic in topics
                ]
            }
        )

        response.raise_for_status()

        logger.info('Получено и заблокировано %s задач', len(response.json()))

        for data in response.json():
            logger.debug(data)
            yield model.ExternalTask(**data)

    def complete_external_task(
        self,
        task: model.ExternalTask,
        **variables
    ) -> None:
        """Отметить задачу выполненной.

        variables - новые переменные, которые будут установлены процессу.
        """

        response = self._session.post(
            self._build_url(
                f'/external-task/{task.id}/complete'
            ),
            json={
                'workerId': self._config.worker_id,
                'variables': {
                    name: {'value': value}
                    for name, value in variables.items()
                }
            }
        )
        response.raise_for_status()

    def _build_url(self, *paths: str, **query_params) -> str:
        """Строит URL запроса исходя из параметров подключения и переданных значений.

        ... code:: python
          >>> self._build_url('/api/', '/v1/', cascade=True)

              http://127.0.0.1:8080/api/v1/?cascade=true
        """
        scheme, netloc, path, params, query, fragment = urlparse(self._config.engine_url)

        for part in paths:
            path = PATH_SEP.join((path.rstrip(PATH_SEP), part.lstrip(PATH_SEP)))

        query = urlencode({**dict(parse_qsl(query)), **query_params})

        return urlunparse((scheme, netloc, path, params, query, fragment))

    # ########################################################################
    # Бизнес-логика
    # ########################################################################
    def process_external_tasks(self, *topics, max_tasks=10) -> Iterable:
        """Получить и обработать доступные внешние задачи.

        max_tasks - ограничение по одновременному количеству задач.
        """

        topics = topics or self.get_external_tasks_topics()
        tasks = self.fetch_and_lock_external_tasks(*topics, max_tasks=max_tasks)
        with ThreadPoolExecutor() as executor:
            yield from executor.map(
                self.process_external_task, tasks
            )

    def process_external_task(self, task: model.ExternalTask) -> Any:
        """Обработать внешнюю задачу.

        Делегируется обработчику, назначенному на топик задачи.
        """

        try:
            handler = self._topic_registry.get(task.topic)
            return handler(task, self)
        except Exception as error:  # pylint: disable=broad-except
            logger.exception('Ошибка обработки задачи %s: %s', task.id, str(error))

    # ########################################################################
    # Прокси-методы регистрации обработчиков
    # ########################################################################
    def register_topic_handler(
        self,
        topic: model.Topic,
        handler: TopicHandler
    ) -> None:
        """Зарегистрировать обработчик топика."""

        return self._topic_registry.register(topic, handler)

    def replace_topic_handler(
        self,
        topic: model.Topic,
        handler: TopicHandler
    ) -> None:
        """Заменить обработчик топика."""

        return self._topic_registry.replace(topic, handler)

    def available(self) -> bool:
        """Проверяет доступность движка."""

        try:
            return self._session.get(
                self._build_url('/engine')
            ).status_code == 200
        except requests.exceptions.RequestException:
            return False
