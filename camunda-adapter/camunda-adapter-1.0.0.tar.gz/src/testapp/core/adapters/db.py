"""In-memory репозитории, имитирующие хранение данных."""

from abc import ABC
from typing import Any, Iterable, List, Union

from testapp.core.domain import model


class AbstractRepository(ABC):

    """Абстрактный репозиторий."""

    _items: Any

    def __init__(self) -> None:
        self._items = []

    def add(self, item: Any) -> None:
        self._items.append(item)

    def get_all_objects(self) -> Iterable[Any]:
        yield from iter(self._items)


class DeclarationsRepository(AbstractRepository):

    """Хранилище заявлений."""

    _items: List[model.Declaration]

    def add(self, item: model.Declaration) -> None:
        assert isinstance(item, model.Declaration)
        return super().add(item)

    def get_all_objects(self) -> Iterable[model.Declaration]:
        return super().get_all_objects()

    def get_by_id(self, id_: str) -> Union[model.Declaration, None]:
        return next(filter(lambda d: d.id == id_, self._items))


declarations_repository = DeclarationsRepository()


class SearchByDeclarationMixin(AbstractRepository):

    """Примесь к хранилищу для поиска по заявлению."""

    def get_by_declaration(
        self, declaration: model.Declaration
    ) -> Union[model.Session, None]:
        return next(
            filter(
                lambda item: item.declaration == declaration,
                self._items
            )
        )


class SessionsRepository(SearchByDeclarationMixin, AbstractRepository):

    """Хранилище заседаний."""

    _items: List[model.Session]


sessions_repository = SessionsRepository()


class NotificationsRepository(SearchByDeclarationMixin, AbstractRepository):

    """Хранилище уведомлений."""

    _items: List[model.Notification]


notifications_repository = NotificationsRepository()


class ComissionsRepository(SearchByDeclarationMixin, AbstractRepository):

    """Хранилище комиссий."""

    _items: List[model.Comission]


comissions_repository = ComissionsRepository()
