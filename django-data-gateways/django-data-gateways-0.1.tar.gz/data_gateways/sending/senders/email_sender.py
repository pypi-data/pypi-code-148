from django.core.mail import send_mail

from .abstract_sender import AbstractSender
from ...reporters.sending_report import SendingReport
from ...message_dao.base_message_dao import BaseMessageDAO
from ...message_builder.abstract_message_builder import AbstractMessageBuilder


class EmailSender(AbstractSender):
    """Отправитель данных на почту"""

    def __init__(
        self, 
        sender_email: str, 
        recipients_emails: list[str], 
        message_builder: AbstractMessageBuilder | None = None,
        subject_template: str | None = None,
        body_template: str | None = None,
    ) -> None:
        """
        Инициализатор класса.
        
        :param sender_email: email отправителя.
        :param recipients_emails: Список email'ов адресатов.
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
        
        self.__sender_email = sender_email
        self.__recipients_emails = recipients_emails

    def send(self, message_dao: BaseMessageDAO) -> SendingReport:
        """
        Отправка данных на почту.

        :param message_dao: Объект доступа к данным.
        :return: Отчет об отправке.
        """

        # Генерация сообщения.
        message_subject, message_body = self.compile_message(message_dao)

        # Пытаемся отправить на почту. 
        # В случае любого исключения логируем ошибку на верхнем уровне.
        send_mail(
            message_subject, 
            message_body, 
            self.__sender_email, 
            self.__recipients_emails,
        )

        return SendingReport(status=SendingReport.Status.OK, sender=self)
