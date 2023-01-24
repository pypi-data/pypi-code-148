from typing import Type

from ..sending.senders.abstract_sender import AbstractSender
from ..sending.strategies.abstract_send_strategy import AbstractSendStrategy


class SenderRegistry:
    """Реестр отправщиков"""

    def __init__(self) -> None:
        """Инициализатор класса"""

        self.__sender_classes: set[Type[AbstractSender]] = set()

    def register(self, sender_class: Type[AbstractSender]) -> None:
        """
        Регистрация нового отправщика.

        :param sender_class: Класс отправщика.
        """

        self.__sender_classes.add(sender_class)

    def unregister(self, sender_class: Type[AbstractSender]) -> None:
        """
        Удаление отправщика из реестра.

        :param sender_class: Класс отправщика.
        """

        self.__sender_classes.remove(sender_class)

    def get_sender_classes(self) -> set[Type[AbstractSender]]:
        """Получение множества отправщиков"""

        return self.__sender_classes


class StrategyRegistry:
    """Реестр стратегий"""

    def __init__(self) -> None:
        """Инициализатор класса"""
        
        self.__strategy_classes: set[Type[AbstractSendStrategy]] = set()

    def register(self, strategy_class: Type[AbstractSendStrategy]) -> None:
        """
        Регистрация новой стратегии.

        :param strategy_class: Класс стратегии.
        """

        self.__strategy_classes.add(strategy_class)

    def unregister(self, strategy_class: Type[AbstractSender]) -> None:
        """
        Удаление стратегии из реестра.

        :param strategy_class: Класс стратегии.
        """

        self.__strategy_classes.remove(strategy_class)

    def get_strategy_classes(self) -> set[Type[AbstractSendStrategy]]:
        """Получение множества стратегий"""

        return self.__strategy_classes
