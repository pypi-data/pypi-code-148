from ...reporters.sending_report import SendingReport
from .abstract_send_strategy import AbstractSendStrategy
from ...message_dao.base_message_dao import BaseMessageDAO


class AllSystemsSendStrategy(AbstractSendStrategy):
    """
    Стратегия отправки данных во все внешние системы.
    """

    description = 'Стратегия отправки сообщения в каждую внешнюю систему'

    def send(self, message_dao: BaseMessageDAO) -> SendingReport:
        """
        Отправка сообщения согласно стратегии.

        :param message_dao: Объект для доступа к данным.
        :return: Отчет об отправке.
        """

        # Получаем отправщиков в текущей стратегии, создаем дефолтный отчет 
        # и список отчетов об отправке у отправщиков.
        senders = self.get_senders()
        report = SendingReport(status=SendingReport.Status.OK, sender=self)
        sender_reports: list[SendingReport] = []

        # Отправляем данные во внешние системы.
        for sender in senders:
            sender_report = sender.send(message_dao)
            sender_reports.append(sender_report)

        # Согласно этой стратегии, отправка считается успешной, если данные 
        # отправлены в каждую внешнюю систему.
        failed_senders: list[SendingReport] = list(filter(
            lambda report: report.status == SendingReport.Status.FAILED, 
            sender_reports
        ))
        if len(failed_senders) > 0:
            report.status = SendingReport.Status.FAILED

        report.nested_reports = sender_reports

        return report
