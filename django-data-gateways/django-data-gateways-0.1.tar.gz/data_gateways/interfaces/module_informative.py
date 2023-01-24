from abc import ABC


class IModuleInformative(ABC):
    """
    Интерфейс для получения информации о модуле.
    """

    name = ''
    description = ''

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__ if cls.name == '' else cls.name

    @classmethod
    def get_description(cls) -> str:
        return cls.description

    @classmethod
    def get_path_to_class(cls) -> str:
        return f'{cls.__module__}.{cls.__name__}'
