from abc import (
    ABC,
    abstractmethod,
)
from typing import Any


class AbstractMessageBuilder(ABC):
    """Абстрактный класс для построения сообщения"""

    def __init__(
        self,
        subject_template: str,
        body_template: str,
    ) -> None:
        """
        Инициализатор класса.

        :param subject_template: Имя шаблона для заголовка.
        :param body_template: Имя шаблона для тела сообщения.
        """

        self._subject_template = subject_template
        self._body_template = body_template

    @abstractmethod
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
        raise NotImplementedError()
