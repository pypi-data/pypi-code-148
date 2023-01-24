from ...reporters.sending_report import SendingReport
from .abstract_send_strategy import AbstractSendStrategy
from ...message_dao.base_message_dao import BaseMessageDAO


class FirstSuccessSystemSendStrategy(AbstractSendStrategy):
    """
    Стратегия отправки данных в первую успешную внешнюю систему.
    """

    description = 'Стратегия отправки сообщения в первую успешную внешнюю систему'

    def send(self, message_dao: BaseMessageDAO) -> SendingReport:
        """
        Отправка сообщения согласно стратегии.

        :param message_dao: Объект для доступа к данным.
        :return: Отчет об отправке.
        """

        # Получаем отправщиков в текущей стратегии, создаем дефолтный отчет 
        # и список отчетов об отправке у отправщиков.
        senders = self.get_senders()
        report = SendingReport(status=SendingReport.Status.FAILED, sender=self)
        sender_reports: list[SendingReport] = []

        # Пытаемся отправить данные в первый успешный вариант.
        for sender in senders:
            sender_report = sender.send(message_dao)
            sender_reports.append(sender_report)

            # Если данные отправились, согласно стратегии, выходим из цикла.
            if sender_report.status == SendingReport.Status.OK:
                report.status = SendingReport.Status.OK
                break

        report.nested_reports = sender_reports

        return report
