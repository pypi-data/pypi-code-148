from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MessageSenderConfig(AppConfig):
    """Конфигурация приложения"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.message_sender'
    verbose_name = _('Отправщик сообщений во внешние системы')
