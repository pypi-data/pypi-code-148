from enum import Enum
from dataclasses import dataclass

from ..interfaces.module_informative import IModuleInformative


# TODO: Отрефакторить! Код ужасен.
@dataclass
class SendingReport:
    """Класс результата отправки данных"""

    class Status(Enum):
        """Статусы отправки данных"""

        OK = 'OK'
        FAILED = 'FAILED'

    status: Status
    sender: IModuleInformative
    error: Exception | None = None
    nested_reports: list['SendingReport'] | None = None

    def build(self, title: str, sep: str = '=', length_sep: int = 35) -> str:
        """
        Создание отчета из данных.

        :param title: Заголовок отчета.
        :param sep: Разделитель отчета.
        :return: Отчет об отправке в виде строки.
        """

        report = self._build()
        result = f'\n{title}\n'
        result += sep * length_sep + '\n'
        result += report + sep * length_sep

        return result

    def _build(self, base_text: str = '') -> str:
        """Детали отчета при печати"""
        
        if self.nested_reports is None:
            result = f'{base_text}{self.sender.get_name()}: Status: {self.status.value}'
            if self.error:
                result += f', Error: {repr(self.error)}'
            result += '\n'
            return result

        nested_reports_text = ''
        for nested_report in self.nested_reports:
            nested_reports_text += nested_report._build(
                base_text + self.sender.get_name() + ' -> '
            )

        return nested_reports_text
