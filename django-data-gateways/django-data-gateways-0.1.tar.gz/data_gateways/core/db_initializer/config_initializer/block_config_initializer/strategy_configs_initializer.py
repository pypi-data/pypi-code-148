from typing import (
    Any,
    Final,
    Iterable,
)

from .....models import (
    StrategyConfig,
    StrategySenderRelation,
)
from .abstract_block_config_initializer import AbstractBlockConfigInitializer


class StrategyConfigsInitializer(AbstractBlockConfigInitializer):
    """Класс для инициализации конфигураций стратегий в БД"""

    __CONFIG_KEY: Final[str] = 'STRATEGY_CONFIGS'

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

    # TODO: В будущем прежде, чем итерироваться по коллекции конфигураций 
    # стратегий, нужно учесть все зависимости, чтобы можно было не 
    # соблюдать порядок конфигураций стратегий в главной конфигурации.
    def init(self) -> None:
        """Метод инициализации"""

        # Создаем списки моделей конфигураций стратегий и отправки и 
        # сконфигурированных отправщиков к ним.
        relation_config_models: list[StrategySenderRelation] = []
        strategy_config_models: list[StrategyConfig] = []

        for strategy_config in self._config:
            # Создаем модель конфигурации стратегии.
            new_strategy_config_model = StrategyConfig(
                name=strategy_config['name'],
                description=strategy_config.get('description', ''),
                module_id=strategy_config['strategy_name'],
                init_params=strategy_config.get('params', dict()),
            )
            strategy_config_models.append(new_strategy_config_model)

            # Создаем модели связи между конфигурацией стратегии и конфигурацией отправщика.
            for relation_config in strategy_config.get('senders', []):
                new_relation = self._get_relation_config(relation_config)
                new_relation.parent_send_strategy = new_strategy_config_model
                relation_config_models.append(new_relation)

        # Создаем все конфигурации стратегий в БД.
        StrategyConfig.objects.bulk_create(strategy_config_models, ignore_conflicts=True)
        
        # Создаем связанные со стратегиями связи с сконфигурированными отправщиками.
        if len(relation_config_models) > 0:
            StrategySenderRelation.objects.bulk_create(relation_config_models, ignore_conflicts=True)

    def _get_relation_config(self, relation_config: dict[str, Any]) -> StrategySenderRelation:
        """
        Получение модели связи между моделью конфигурации стратегии 
        и моделью конфигурации отправщика.

        :param relation_config: Конфигурация связи.
        :return: Модель конфигурации связи.
        """

        new_relation = StrategySenderRelation(
            serial_number=relation_config['serial_number'],
            enabled=relation_config.get('enabled', True),
        )

        # В связи может хранится либо конфигурация отправщика, либо конфигурация другой стратегии.
        error = AttributeError(
            'Необходимо указать либо параметр sender_config, либо '
            'параметр strategy_config.'
        )
        if (
            relation_config.get('sender_config') is not None and 
            relation_config.get('strategy_config') is not None
        ):
            raise error
        elif relation_config.get('strategy_config'):
            new_relation.send_strategy_config_id = relation_config['strategy_config']
        elif relation_config.get('sender_config'):
            new_relation.sender_config_id = relation_config['sender_config']
        else:
            raise error

        return new_relation
