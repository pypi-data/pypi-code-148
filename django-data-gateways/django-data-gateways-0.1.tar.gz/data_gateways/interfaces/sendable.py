from abc import (
    ABC,
    abstractmethod,
)

from ..reporters.sending_report import SendingReport
from ..message_dao.base_message_dao import BaseMessageDAO


class ISendable(ABC):
    """
    Интерфейс отправляемого объекта.
    """

    @abstractmethod
    def send(self, message_dao: BaseMessageDAO) -> SendingReport:
        """
        Метод отправки данных.

        :param message_dao: Объект для доступа к данным.
        :return: Отчет об отправке со статусом и деталями.
        """
        raise NotImplementedError()
