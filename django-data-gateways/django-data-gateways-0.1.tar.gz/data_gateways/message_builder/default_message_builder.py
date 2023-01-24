from typing import Any
from django.template.loader import render_to_string

from .abstract_message_builder import AbstractMessageBuilder


class DefaultMessageBuilder(AbstractMessageBuilder):
    """Класс для построения сообщения из шаблонных файлов"""

    def build(
        self,
        subject_data: dict[str, Any] | None = None,
        body_data: dict[str, Any] | list[dict[str, Any]] | None = None,
        block_separator: str = '\n',
    ) -> tuple[str, str]:
        """
        Метод построения сообщения.

        :param subject_data: Данные для заголовка.
        :param body_data: 
            Данные для тела сообщения. Может передаваться как один элемент, 
            так и список из нескольких данных, если в одном сообщение нужно 
            отправить сразу несколько объектов.
        :param block_separator: Разделитель блоков сообщения. Используется только если body_data является списком.
        :return: Кортеж из заголовка и тела сообщения в виде строк.
        """

        # Ковертируем словарь с данными для заголовка в текст.
        message_subject = render_to_string(
            template_name=self._subject_template,
            context=subject_data,
        )
        # Удаляем двойные переносы строк.
        message_subject = self._normalize_line_breaks(message_subject)

        # В зависимости от типа переданных данных конвертируем данные для 
        # тела сообщения в строку.
        message_body = ''
        if isinstance(body_data, list):
            for message_data in body_data:
                part_message = render_to_string(
                    template_name=self._body_template, 
                    context=message_data,
                )
                part_message = self._normalize_line_breaks(part_message)
                message_body += part_message + block_separator
        elif body_data is not None:
            message_body = render_to_string(
                template_name=self._body_template, 
                context=body_data,
            )
            message_body = self._normalize_line_breaks(message_body)
        else:
            message_body = render_to_string(self._body_template)

        return message_subject, message_body

    def _normalize_line_breaks(self, string: str) -> str:
        """
        Нормализация переносов строк.

        Заменяет все множественные переносы на один перенос строки.

        :param string: Исходная строка.
        :return: Строка без лишних переносов строк.
        """

        while string.find('\n\n') != -1:
            string = string.replace('\n\n', '\n')
        
        return string
