"""Набор тестов для проверки адаптера к Camunda."""

from pathlib import Path
from typing import List
import logging
import unittest

from more_itertools import consume, ilen
import requests

from testapp import core
from testapp.core.adapters.db import comissions_repository as comissions
from testapp.core.adapters.db import declarations_repository as declarations
from testapp.core.adapters.db import notifications_repository as notifications
from testapp.core.adapters.db import sessions_repository as sessions
from testapp.core.domain.model import STATUS_PENDING, Declaration

from camunda_adapter import Adapter, Config
from camunda_adapter.adapters import TopicHandlerRegistry
from camunda_adapter.domain import model
from camunda_adapter.utils import cleanup


logger = logging.getLogger(__name__)


PROCESS_DEFINITION_ID = 'camunda_adapter_test'

DECLARATIONS_COUNT = 100

logger.info('PROCESS_DEFINITION_ID: %s', PROCESS_DEFINITION_ID)

assert core.adapter is not None


class TestAdapter(unittest.TestCase):

    """Набор тестов для проверки адаптера к Camunda."""

    config: Config
    adapter: Adapter
    definition: model.Definition

    @classmethod
    def _setup_deployment(cls) -> None:

        assert core.adapter is not None

        cls.adapter = core.adapter

        cleanup(cls.adapter)
        try:
            cls.definition = cls.adapter.get_definition_by_key(PROCESS_DEFINITION_ID)
            logger.info('Definition exists')
        except ValueError:
            cls.definition = cls.adapter.create_deployment(
                PROCESS_DEFINITION_ID,
                Path(__file__).parent / 'diagrams' / f'{PROCESS_DEFINITION_ID}.bpmn'
            )
            logger.info('Definition deployed')

    @classmethod
    def setUpClass(cls):
        try:
            cls._setup_deployment()
        except requests.exceptions.RequestException as e:
            logger.exception('Can not deploy Camunda')
            response = getattr(e, 'response', None)
            if response is not None:
                error = model.Error(**response.json())
                logger.error(error)
            raise

    @classmethod
    def tearDownClass(cls):
        """Очистка."""
        cleanup(cls.adapter)

    # @debug_requests
    def test_camunda_adapter(self) -> None:
        assert isinstance(self.adapter, Adapter)

        consume(map(declarations.add, (Declaration() for _ in range(DECLARATIONS_COUNT))))

        # Все ID уникальны
        unique_ids_count = len(set(d.id for d in declarations.get_all_objects()))
        self.assertEqual(unique_ids_count, DECLARATIONS_COUNT)

        # Выбор процесса для запуска
        definition: model.Definition = self.adapter.get_definition_by_key(PROCESS_DEFINITION_ID)
        self.assertIsInstance(definition, model.Definition)

        def send_messages(*declarations_: Declaration) -> None:
            for declaration in declarations_:
                with self.subTest(declaration):
                    message = model.Message(
                        messageName='DeclarationReceived',
                        businessKey=f'attestation-declaration-{declaration.id}',
                        processVariables={
                            name: model.Variable(value=value)
                            for name, value in declaration.dict(include={'id'}).items()
                        }
                    )
                    message_results: List[model.MessageResult] = list(self.adapter.message(message))
                    self.assertEqual(len(message_results), 1)

                    process = message_results[0].processInstance

                    assert process is not None

                    self.assertIsInstance(process, model.Process)

                    self.assertIn(PROCESS_DEFINITION_ID, process.definitionId)
                    self.assertIsNotNone(process.id)

                    processes = list(self.adapter.get_processes())
                    self.assertGreater(len(processes), 0)

                    self.assertIn(process, processes)

                    # Проверка наличия внешних (по отн. к Camunda) задач
                    external_tasks = list(self.adapter.get_external_tasks(definition=definition))
                    self.assertGreater(len(external_tasks), 0)

        # Запуск процесса через сообщение
        send_messages(*declarations.get_all_objects())

        while ilen(self.adapter.get_external_tasks(definition=definition)):
            consume(self.adapter.process_external_tasks())

        def get_count(attr):
            """Количество заявлений с attr=True."""
            return ilen(
                filter(
                    lambda x: bool(getattr(x, attr, None)) is True,
                    declarations.get_all_objects()
                )
            )

        # Соответствие состояния объекта его статусу
        # означает прохождение всех переходов модели.
        for declaration in declarations.get_all_objects():
            with self.subTest(declaration):

                self.assertNotEqual(declaration.status, STATUS_PENDING)

                if declaration.rejected:
                    self.assertEqual(declaration.status, 'Отказано')

                if declaration.withdrawn:
                    self.assertEqual(declaration.status, 'Отозвано')

                if declaration.needs_work:
                    self.assertIn(declaration.status, ['На доработку', 'Отозвано'])

                if not any((declaration.rejected, declaration.withdrawn, declaration.needs_work)):
                    self.assertIn(declaration.status, ['Рассмотрено'])

        # Добавлены уведомления для заявлений с доработками
        self.assertGreaterEqual(
            ilen(notifications.get_all_objects()),
            get_count('needs_work')
        )

        # Проведены заседания и комиссии для рассмотренных заявлений
        for declaration in filter(
            lambda declaration: declaration.status == 'Рассмотрено',
            declarations.get_all_objects()
        ):
            with self.subTest(declaration):
                self.assertIsNotNone(sessions.get_by_declaration(declaration))
                self.assertIsNotNone(comissions.get_by_declaration(declaration))


class TestTopicRegistry(unittest.TestCase):

    """Набор тестов для проверки реестра обработчиков."""

    def test_topic_registry(self):

        def handler1(task, adapter):  # pylint:disable=unused-argument
            pass

        def handler2(task, adapter):  # pylint:disable=unused-argument
            pass

        topic = model.Topic(name='test-topic')

        registry = TopicHandlerRegistry()

        registry.register(topic, handler1)
        self.assertIs(handler1, registry.get(topic))

        registry.replace(topic, handler2)
        self.assertIs(handler2, registry.get(topic))

        not_registered_topic = model.Topic(name='not-registered-topic')
        with self.assertRaises(ValueError):
            registry.get(not_registered_topic)

        occasionally_same_topic = model.Topic(name='test-topic')
        with self.assertRaises(ValueError):
            registry.register(occasionally_same_topic, handler1)
