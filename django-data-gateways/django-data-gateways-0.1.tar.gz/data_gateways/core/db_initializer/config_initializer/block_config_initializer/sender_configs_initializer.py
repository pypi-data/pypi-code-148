from typing import (
    Any,
    Final,
    Iterable,
)

from .....models import SenderConfig
from .abstract_block_config_initializer import AbstractBlockConfigInitializer


class SenderConfigsInitializer(AbstractBlockConfigInitializer):
    """Класс для инициализации конфигураций отправщиков в БД"""

    __CONFIG_KEY: Final[str] = 'SENDER_CONFIGS'

    def __init__(self, config: object) -> None:
        """
        Инициализатор класса.

        :param config: Конфигурация блока.
        """

        self._config: Iterable[dict[str, Any]] = config

    @classmethod
    def get_config_key(cls) -> str:
        """
        Получение ключа, по которому будет искаться нужный 
        блок конфигурации в главной конфигурации.
        """

        return cls.__CONFIG_KEY

    def init(self) -> None:
        """Метод инициализации"""

        # Создаем список моделей конфигураций отправщиков.
        sender_config_models: list[SenderConfig] = []
        for sender_config in self._config:
            new_sender_config_model = SenderConfig(
                name=sender_config['name'],
                description=sender_config.get('description', ''),
                module_id=sender_config['sender_name'],
                init_params=sender_config.get('params', dict()),
            )
            sender_config_models.append(new_sender_config_model)

        SenderConfig.objects.bulk_create(sender_config_models, ignore_conflicts=True)
