from abc import (
    ABC,
    abstractmethod,
)
from typing import Type

from ..base_sendable_object import BaseSendableObject
from ...reporters.sending_report import SendingReport
from ...message_dao.base_message_dao import BaseMessageDAO
from ...message_builder.default_message_builder import DefaultMessageBuilder
from ...message_builder.abstract_message_builder import AbstractMessageBuilder


class AbstractSender(BaseSendableObject, ABC):
    """Абстрактный класс отправителя данных"""
    
    default_message_builder_class: Type[AbstractMessageBuilder] = DefaultMessageBuilder

    def __init__(
        self, 
        message_builder: AbstractMessageBuilder | None = None,
        subject_template: str | None = None,
        body_template: str | None = None,
    ) -> None:
        """
        Инициализатор класса.

        :param message_builder: 
            Объект билдера сообщения на основе данных. Если None, 
            используется дефолтный билдер сообщений.
        :param subject_template:
            Путь до шаблона темы сообщения. Нужен, если не передан параметр message_builder.
            Если message_builder передан, параметр игнорируется.
        :param body_template: 
            Путь до шаблона тела сообщения. Нужен, если не передан параметр message_builder.
            Если message_builder передан, параметр игнорируется.
        """

        super().__init__()

        # Если нет объекта билдера сообщения, создаем из дефолтного класса 
        # на основе переданных путей до шаблонов.
        if message_builder is None:
            # Если и путей до шаблонов нет, поднимаем исключение.
            if subject_template is None or body_template is None:
                raise TypeError(
                    'subject_template и body_template не могут принимать значение None. \n'
                    'Необходимо указать либо объект сборщика сообщения, либо пути до '
                    'шаблонов с сообщениями.'
                )
            self.__message_builder = self.default_message_builder_class(
                subject_template=subject_template,
                body_template=body_template,
            )
        # Иначе берем тот, что передали.
        else:
            self.__message_builder = message_builder

    def get_message_builder(self) -> AbstractMessageBuilder:
        """Получение объекта билдера сообщений"""

        return self.__message_builder

    def compile_message(self, message_dao: BaseMessageDAO) -> tuple[str, str]:
        """
        Компиляция сообщения в строку на основе данных в DAO-объекте.

        :param message_dao: Объект для получения доступа к данным.
        :return: Заголовок сообщения и тело сообщения в виде строк.
        """

        message_builder = self.get_message_builder()

        return message_builder.build(
            subject_data=message_dao.get_subject_data(),
            body_data=message_dao.get_body_data(),
        )

    @abstractmethod
    def send(self, message_dao: BaseMessageDAO) -> SendingReport:
        raise NotImplementedError()
