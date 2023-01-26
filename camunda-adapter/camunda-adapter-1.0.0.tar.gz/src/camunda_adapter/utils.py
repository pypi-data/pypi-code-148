"""Набор инструментов адаптера."""

import logging

from .adapters import Adapter


logger = logging.getLogger(__name__)


def cleanup(adapter: Adapter):

    """Полная очистка.

    Выбирает и удаляет все развёртывания и определения процессов и их активные задачи.
    """

    logger.info('Cleanup: removing definitions')
    for definition in adapter.get_definitions():
        logger.info('Removing %s', definition)
        adapter.rm_definition(definition, cascade=True)

    logger.info('Cleanup: removing deployments')
    for deployment in adapter.get_deployments():
        logger.info('Removing %s', deployment)
        adapter.rm_deployment(deployment, cascade=True)

    assert not list(adapter.get_deployments())
    assert not list(adapter.get_definitions())

    logger.info('Cleanup: done')
