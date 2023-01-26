"""Обработчики внешних задач."""

import logging
import random

from more_itertools.recipes import consume

from testapp.core.adapters.db import comissions_repository as comissions
from testapp.core.adapters.db import declarations_repository as declarations
from testapp.core.adapters.db import notifications_repository as notifications
from testapp.core.adapters.db import sessions_repository as sessions
from testapp.core.domain import model

from camunda_adapter.adapters import Adapter
from camunda_adapter.domain import model as camunda


logger = logging.getLogger(__name__)


set_stage_topic = camunda.Topic(name='set-stage')


def set_stage(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)
    assert isinstance(task.variables['stage'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    declaration.stage = task.variables['stage'].value
    logger.info(
        'Установлен этап "%s" заявлению "%s"',
        task.variables['stage'].value, declaration.id
    )

    return adapter.complete_external_task(task)


set_status_topic = camunda.Topic(name='set-status')


def set_status(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)
    assert isinstance(task.variables['status'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    declaration.status = task.variables['status'].value

    adapter.complete_external_task(task)

    logger.info(
        'Установлен статус "%s" заявлению "%s"',
        task.variables['status'].value, declaration.id
    )


def get_bool(from_=(True, False)):
    return bool(random.choice(from_))  # noqa


def imitate_secretary(declaration: model.Declaration):
    """Рандомно отклоняем, возвращаем или принимаем заявление."""

    # Для вернувшихся заявлений сбрасываем результаты проверки
    declaration.approved = declaration.rejected = declaration.needs_work = None

    declaration.rejected = not get_bool(from_=range(10))  # ~10%

    if not declaration.rejected:
        declaration.needs_work = not get_bool(from_=range(10))  # ~10%

    declaration.approved = (
        not declaration.rejected and
        not declaration.needs_work
    )


def declaration_withdrawn(declaration):
    declaration.withdrawn = not get_bool(from_=range(20))  # ~5% за проверку
    logger.info('Отозвано заявление "%s"', declaration.id)


def check_withdrawn(declaration, adapter: Adapter):
    declaration_withdrawn(declaration)
    if declaration.withdrawn:
        message = camunda.Message(
            messageName='DeclarationWithdrawn',
            businessKey=f'attestation-declaration-{declaration.id}',
            processVariables={
                name: camunda.Variable(value=value)
                for name, value in declaration.dict(include={'id'}).items()
            }
        )
        consume(adapter.message(message))
    return declaration.withdrawn


approve_declaration_topic = camunda.Topic(name='approve-declaration')


def approve_declaration(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    if check_withdrawn(declaration, adapter):
        return

    imitate_secretary(declaration)

    logger.info(
        (
            'Результаты проверки секретарём: '
            'принято: %s, отклонено: %s, на доработку: %s'
        ),
        declaration.approved, declaration.rejected, declaration.needs_work
    )
    return adapter.complete_external_task(
        task,
        approved=declaration.approved,
        rejected=declaration.rejected,
        needs_work=declaration.needs_work
    )


get_withdrawn_topic = camunda.Topic(name='get-withdrawn')


def get_withdrawn(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    # Небольшая вероятность отзыва заявления
    if check_withdrawn(declaration, adapter):
        return

    return adapter.complete_external_task(task, withdrawn=declaration.withdrawn)


set_experts_topic = camunda.Topic(name='set-experts')


def set_experts(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    available_experts = list(range(1, 10))

    if check_withdrawn(declaration, adapter):
        return

    if not get_bool(from_=range(20)):
        logger.info('Ожидание назначения экспертов: %s', task.id)
        return

    declaration.experts = list(set(random.choice(available_experts) for _ in range(7)))
    logger.info('Назначаются эксперты: %s', declaration.experts)
    return adapter.complete_external_task(task, expert_ids=declaration.experts)


notify_needs_work_topic = camunda.Topic(name='notify-needs-work')


def notify_needs_work(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    logger.info('Уведомление о доработке заявления "%s"', declaration.id)
    notifications.add(model.Notification(declaration=declaration))
    return adapter.complete_external_task(task)


expertise_expert_validate_declaration_topic = camunda.Topic(name='expertise-expert-validate-declaration')


def expertise_expert_validate_declaration(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    expert_id: camunda.Variable = task.variables['expert_id']
    assert expert_id.type in camunda.REVERSE_MAP

    logger.info('Ознакомление: эксперт %s, заявление %s, задача %s', expert_id.value, declaration.id, task.id)

    assert camunda.REVERSE_MAP[expert_id.type](expert_id.value), declaration.experts

    return adapter.complete_external_task(task, expertise_declaration_valid=get_bool())


expertise_expert_do_expertise_topic = camunda.Topic(name='expertise-expert-do-expertise')


def expertise_expert_do_expertise(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    expert_id: camunda.Variable = task.variables['expert_id']
    assert expert_id.type in camunda.REVERSE_MAP

    logger.info('Экспертиза: эксперт %s, заявление %s, задача %s', expert_id.value, declaration.id, task.id)

    assert camunda.REVERSE_MAP[expert_id.type](expert_id.value), declaration.experts

    return adapter.complete_external_task(task, expertise_declaration_valid=get_bool())


set_session_topic = camunda.Topic(name='set-session')


def set_session(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    logger.info('Назначение сессии "%s"', declaration.id)
    sessions.add(model.Session(declaration=declaration))
    return adapter.complete_external_task(task)


set_comission_results_topic = camunda.Topic(name='set-comission-results')


def set_comission_results(task: camunda.ExternalTask, adapter: Adapter):
    assert isinstance(task.variables['id'].value, str)

    declaration = declarations.get_by_id(task.variables['id'].value)
    assert declaration is not None

    logger.info('Назначение результатов комиссии "%s"', declaration.id)
    comissions.add(model.Comission(declaration=declaration))
    return adapter.complete_external_task(task)
