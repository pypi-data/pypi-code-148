"""Bootstrap-модуль для настройки приложения."""

# pylint: disable=import-outside-toplevel

from django.apps import AppConfig as AppConfigBase

from camunda_adapter.adapters import Adapter
from camunda_adapter.config import Config


class AppConfig(AppConfigBase):

    """Подключение django-app к django-project."""

    name = __package__

    def ready(self):
        self._setup_bpmn()

    def _setup_bpmn(self):
        from testapp import core

        from . import services

        core.config = Config()
        core.adapter = Adapter(core.config)

        for topic, handler in (
            (services.set_stage_topic, services.set_stage),
            (services.set_status_topic, services.set_status),
            (services.approve_declaration_topic, services.approve_declaration),
            (services.get_withdrawn_topic, services.get_withdrawn),
            (services.set_experts_topic, services.set_experts),
            (services.notify_needs_work_topic, services.notify_needs_work),
            (services.expertise_expert_validate_declaration_topic, services.expertise_expert_validate_declaration),
            (services.expertise_expert_do_expertise_topic, services.expertise_expert_do_expertise),
            (services.set_session_topic, services.set_session),
            (services.set_comission_results_topic, services.set_comission_results)
        ):
            core.adapter.register_topic_handler(topic, handler)
