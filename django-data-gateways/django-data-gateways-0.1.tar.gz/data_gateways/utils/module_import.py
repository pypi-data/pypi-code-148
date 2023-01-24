import sys
import importlib.util
from typing import Type
from types import ModuleType


def lazy_module_import(module_name: str) -> ModuleType:
    """
    Функция загрузки Python-модуля по его названию.

    :param name: Имя модуля в виртуальном окружении.
    """

    spec = importlib.util.find_spec(module_name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    loader.exec_module(module)
    
    return module


def lazy_class_import(path_to_class: str) -> Type:
    """
    Функция загрузки Python-класса по его названию.

    :param name: Имя модуля в виртуальном окружении.
    """

    path_elements = path_to_class.split('.')
    class_name = path_elements.pop(-1)
    module_path = '.'.join(path_elements)

    return getattr(lazy_module_import(module_path), class_name)
