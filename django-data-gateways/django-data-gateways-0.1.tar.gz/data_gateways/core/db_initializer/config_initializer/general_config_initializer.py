from typing import (
    Any,
    Type,
)

from .block_config_initializer import AbstractBlockConfigInitializer
from .block_config_initializer import SenderConfigsInitializer
from .block_config_initializer import StrategyConfigsInitializer
from .block_config_initializer import DataGatewayConfigsInitializer


class GeneralConfigInitializer:
    """
    Класс для инициализации конфигураций стратегий, отправщиков и шлюзов данных в БД.
    """

    # Кортеж классов, отвечающих за инициализацию определенного блока конфигурации.
    __BLOCK_CONFIG_INITIALIZER_CLASSES: tuple[Type[AbstractBlockConfigInitializer]] = (
        SenderConfigsInitializer,
        StrategyConfigsInitializer,
        DataGatewayConfigsInitializer,
    )

    def init(self, config: dict[str, Any]) -> None:
        """
        Инициализация конфигураций стратегий, отправщиков и шлюзов в БД.

        :param config: Словарь со всеми конфигурациями.
        """

        for init_class in self.__BLOCK_CONFIG_INITIALIZER_CLASSES:
            block_config: object | None = config.get(init_class.get_config_key())
            if block_config is None:
                continue
            initializer = init_class(block_config)
            initializer.init()
