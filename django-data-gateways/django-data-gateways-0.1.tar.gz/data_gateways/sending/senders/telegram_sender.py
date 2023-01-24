from typing import Any
from telebot import TeleBot

from .abstract_sender import AbstractSender
from ...reporters.sending_report import SendingReport
from ...message_dao.base_message_dao import BaseMessageDAO
from ...message_builder.abstract_message_builder import AbstractMessageBuilder


class TelegramSender(AbstractSender):
    """Отправитель данных в Telegram"""

    def __init__(
        self, 
        bot_token: str, 
        group_id: str, 
        message_builder: AbstractMessageBuilder | None = None,
        subject_template: str | None = None,
        body_template: str | None = None,
    ) -> None:
        """
        Инициализатор класса.
        
        :param bot_token: Токен telegram-бота.
        :param group_id: ID telegram-группы.
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

        super().__init__(message_builder, subject_template, body_template)
        
        self.__bot = TeleBot(bot_token)
        self.__bot.config['api_key'] = bot_token
        self.__group_id = group_id

    def send(self, message_dao: BaseMessageDAO) -> SendingReport:
        """
        Отправка данных в telegram-группу.

        :param message_dao: Объект доступа к данным.
        :return: Объект отчета об отправке.
        """

        # Генерация сообщения.
        message_subject, message_body = self.compile_message(message_dao)

        result_message = message_subject + '\n\n' + message_body

        # Пытаемся отправить сообщение в telegram.
        response: dict[str, Any] = self.__bot.send_message(
            chat_id=self.__group_id,
            text=result_message,
        )

        # Вслучае ошибки поднимаем исключение.
        if not response['ok']:
            raise Exception(response['error'])

        return SendingReport(status=SendingReport.Status.OK, sender=self)
