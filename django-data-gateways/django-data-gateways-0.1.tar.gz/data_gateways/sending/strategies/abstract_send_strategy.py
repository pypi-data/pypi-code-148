from abc import (
    ABC,
    abstractmethod,
)

from ..base_sendable_object import BaseSendableObject
from ...reporters.sending_report import SendingReport
from ...message_dao.base_message_dao import BaseMessageDAO


class AbstractSendStrategy(BaseSendableObject, ABC):
    """
    Класс абстрактной стратегии отправки сообщения.
    """

    def __init__(
        self, 
        senders: list[BaseSendableObject],
    ) -> None:
        """
        Инициализатор класса.

        :param senders: Список отправителей данных.
        """

        super().__init__()

        self.__senders = senders

    def get_senders(self) -> list[BaseSendableObject]:
        """Получение списка объектов отправителей"""

        return self.__senders

    @abstractmethod
    def send(self, message_dao: BaseMessageDAO) -> SendingReport:
        raise NotImplementedError()
