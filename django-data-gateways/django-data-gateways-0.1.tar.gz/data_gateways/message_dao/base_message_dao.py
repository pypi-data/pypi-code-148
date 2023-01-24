from typing import Any


class BaseMessageDAO:
    """Базовый класс для доступа к данным сообщения"""

    def __init__(
        self, 
        data: dict[str, Any] | list[dict[str, Any]],
        body_data_key: str | None = None,
        subject_data_key: str | None = None, 
    ) -> None:
        """
        Инициализатор класса.

        :param data: 
            Данные в виде словаря. Словарь может иметь любую структуру. 
            Либо же просто список с данными для отправки.
        :param message_data_key: 
            Строка, обозначающая ключ в словаре `data`, под которым лежит 
            словарь одинарной вложенности с данными для сообщения либо 
            список таких словарей.
        :param subject_data_key:
            Если у нас есть данные для заголовка, мы можем их передать.
            Если нет, DAO-объект будет возвращать None при get_subject_data().
        """

        self.__data = data
        self.__subject_data_key = subject_data_key
        self.__body_data_key = body_data_key

    def get_data(self) -> dict:
        """Получение исходных данных"""
        
        return self.__data

    def get_subject_data(self) -> dict[str, Any] | None:
        """Получение данных для заголовка сообщения"""

        if self.__subject_data_key is None:
            return None
        
        return self.__data[self.__subject_data_key]

    def get_body_data(self) -> dict[str, Any] | list[dict[str, Any]]:
        """Получение данных для тела сообщения"""
        
        if self.__body_data_key is None:
            return self.__data
        
        return self.__data[self.__body_data_key]
