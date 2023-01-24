from typing import (
    Final,
    Iterable,
)

from .....models import DataGateway
from .abstract_block_config_initializer import AbstractBlockConfigInitializer


class DataGatewayConfigsInitializer(AbstractBlockConfigInitializer):
    """Класс для инициализации конфигураций шлюзов данных в БД"""

    __CONFIG_KEY: Final[str] = 'DATA_GATEWAYS'

    def __init__(self, config: object) -> None:
        """
        Инициализатор класса.

        :param config: Конфигурация блока.
        """

        self._config: Iterable[dict[str, str]] = config

    @classmethod
    def get_config_key(cls) -> str:
        """
        Получение ключа, по которому будет искаться нужный 
        блок конфигурации в главной конфигурации.
        """

        return cls.__CONFIG_KEY

    def init(self) -> None:
        """Метод инициализации"""

        # Создаем список моделей конфигураций шлюзов данных.
        data_gateway_config_models: list[DataGateway] = []
        for data_gateway_config in self._config:
            new_data_gateway_model = DataGateway(
                name=data_gateway_config['name'],
                description=data_gateway_config.get('description', ''),
            )
            if data_gateway_config.get('strategy_config'):
                new_data_gateway_model.send_strategy_id = data_gateway_config['strategy_config']
            data_gateway_config_models.append(new_data_gateway_model)

        DataGateway.objects.bulk_create(data_gateway_config_models, ignore_conflicts=True)
