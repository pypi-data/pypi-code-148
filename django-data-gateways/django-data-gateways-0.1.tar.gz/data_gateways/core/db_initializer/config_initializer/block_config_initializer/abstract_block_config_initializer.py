from abc import (
    ABC,
    abstractmethod,
)


class AbstractBlockConfigInitializer(ABC):
    """
    Абстрактный класс инициализатора блока конфигурации в БД.
    """

    @abstractmethod
    def __init__(self, config: object) -> None:
        """
        Инициализатор класса.

        :param config: Конфигурация блока.
        """
        raise NotImplementedError()

    @abstractmethod
    def init(self) -> None:
        """Метод инициализации"""
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def get_config_key(cls) -> str:
        """
        Получение ключа, по которому будет искаться нужный 
        блок конфигурации в главной конфигурации.
        """
        raise NotImplementedError()
