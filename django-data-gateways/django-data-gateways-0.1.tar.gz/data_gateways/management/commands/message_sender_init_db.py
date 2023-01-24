import importlib
from django.conf import settings
from django.core.management.base import (
    BaseCommand,
    CommandError,
)

from ... import (
    sender_registry,
    strategy_registry,
)
from ...models import (
    SenderModule,
    StrategyModule,
)
from ...core.db_initializer import (
    ModuleSynchronizer,
    GeneralConfigInitializer,
)


class Command(BaseCommand):
    """Команда для создания в БД периодических задач"""

    def handle(self, *args, **kwargs) -> None:
        """Обработчик команды"""

        if not hasattr(settings, 'MESSAGE_SENDER'):
            raise CommandError(
                'При использовании приложения отправщика сообщений необходимо указать '
                'настройки в файле settings.py'
            )

        # Загрузим модули, в которых пользователи регистрируют своих отправщиков и стратегии.
        for app_name in settings.INSTALLED_APPS:
            try:
                importlib.import_module(f'{app_name}.{settings.MESSAGE_SENDER["INIT_FILE_NAME"]}')
            except:
                pass

        # Синхронизируем информацию о зарегистрированных модулях отправщиков и стратегий в БД.
        module_synchronizer = ModuleSynchronizer()
        module_synchronizer.synchronize(SenderModule, sender_registry.get_sender_classes())
        module_synchronizer.synchronize(StrategyModule, strategy_registry.get_strategy_classes())

        # Инициализируем в БД дефолтные конфигурации отправщиков, стратегий и шлюзов данных, указанынх 
        # в settings.py.
        if hasattr(settings, 'MESSAGE_SENDER'):
            config_initializer = GeneralConfigInitializer()
            config_initializer.init(settings.MESSAGE_SENDER)
