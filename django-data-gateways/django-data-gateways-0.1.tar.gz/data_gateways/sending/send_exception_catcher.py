from typing import (
    Any,
    Type,
    Final,
    Callable,
)
from abc import ABCMeta
from functools import wraps

from ..reporters.sending_report import SendingReport


class SendExceptionCatcher(type):
    """
    Мета-класс, делающий метод `send` в классе "неубиваемым".

    Т.е. метод `send` никогда не выкинет исключения, а вернет вместо этого 
    объект отчета класса `SendingReport` со статусом `SendingReport.Status.FAILED` 
    и подробностями об ошибке.
    """

    _DECORATING_METHOD_NAME: Final[str] = 'send'

    def __new__(
        cls,
        name: str,
        bases: tuple[Type, ...],
        attrs: dict[str, Any],
        **kwargs,
    ):
        """
        Конструктор класса.

        :param cls: Текущий класс.
        :param name: Имя создаваемого класса.
        :param bases: Кортеж классов, от которых наследуется создаваемый класс.
        :param attrs: Словарь со всеми атрибутами создаваемого класса (методы и поля).
        """

        send_method: Callable | None = attrs.get(cls._DECORATING_METHOD_NAME)
        if send_method is None:
            raise AttributeError(
                f'Чтобы использовать мета-класс {cls.__name__}, необходимо определить '
                f'у зависимого класса метод {cls._DECORATING_METHOD_NAME}.'
            )

        attrs[cls._DECORATING_METHOD_NAME] = cls.__catcher(send_method)

        return super().__new__(cls, name, bases, attrs, **kwargs)

    @staticmethod
    def __catcher(method: Callable) -> Callable:
        """
        Декоратор для перехвата всех ошибок.

        :param method: Декорируемый метод.
        :return: Декорированный метод.
        """

        @wraps(method)
        def inner(self, *args, **kwargs) -> SendingReport:
            """Перехват всех ошибок и формирование отчета"""

            # Пытаемся выполнить исходный метод.
            try:
                sending_report: SendingReport = method(self, *args, **kwargs)
            # Если ошибка возникла из-за того, что пользователь класса не реализовал 
            # метод, то дальше поднимаем эту ошибку.
            except NotImplementedError:
                raise
            # Все остальные ошибки перехватываем и создаем нужный отчет.
            except Exception as e:
                sending_report = SendingReport(
                    status=SendingReport.Status.FAILED,
                    sender=self,
                    error=e,
                )

            return sending_report

        return inner


class AbstractSendExceptionCatcher(SendExceptionCatcher, ABCMeta):
    """
    Тот же самый класс `SendExceptionCatcher`, но для применения у 
    абстрактных классов. Это необходимо для того, чтобы не возникало 
    конфилктов мета-классов.
    """
    pass
