from typing import (
    Type,
    Iterable,
)
from django.db.transaction import atomic

from ...models import Module
from ...interfaces import IModuleInformative


class ModuleSynchronizer:
    """
    Класс для синхронизации записей в БД о модулях с информация 
    в коде.

    Получает на вход конкретную модель для хранения информации о модуле и 
    последовательность классов, имплементирующих интерфейс получения данных 
    о модуле. Производит синхронизацию данных в последовательности и в БД.
    """

    def synchronize(
        self,
        model: Type[Module],
        classes: Iterable[Type[IModuleInformative]],
    ) -> None:
        """
        Метод синхронизации данных о модулях для переданной модели.

        :param model: Модель для хранения информации о модуле.
        :param classes: 
            Классы, имплементирующие интерфейс `IModuleInformative`.
        """

        # Создаем список моделей с данными о модулях.
        models = [
            model(
                name=_class.get_name(),
                description=_class.get_description(),
                module_path=_class.get_path_to_class(),
            )
            for _class in classes
        ]

        with atomic():
            # Получаем модули из БД.
            db_modules: set[model] = set(model.objects.all())

            # Определяем множества модулей для удаления и создания.
            deleting_modules_id: tuple[int] = tuple([
                _model.pk 
                for _model in db_modules.difference(set(models))
            ])
            creating_modules: set[model] = set(models).difference(db_modules)

            # Удаляем и создаем только те записи, которые нужно.
            model.objects.filter(pk__in=deleting_modules_id).delete()
            model.objects.bulk_update(models, fields=('module_path', ))
            model.objects.bulk_create(creating_modules)
