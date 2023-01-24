from abc import (
    ABC,
    abstractmethod,
)

from ..interfaces import (
    ISendable,
    IModuleInformative,
)
from ..message_dao import BaseMessageDAO
from ..reporters.sending_report import SendingReport
from .send_exception_catcher import AbstractSendExceptionCatcher


class BaseSendableObject(
    ISendable, 
    IModuleInformative, 
    ABC,
    metaclass=AbstractSendExceptionCatcher,
):
    """
    Базовый абстрактный класс для всех объектов, которые 
    обладаются поведением отправищков.
    """

    @abstractmethod
    def send(self, message_dao: BaseMessageDAO) -> SendingReport:
        """
        Метод отправки данных.

        :param message_dao: Класс для доступа к данным.
        :return: Отчет об отправке со статусом и деталями.
        """
        raise NotImplementedError()
