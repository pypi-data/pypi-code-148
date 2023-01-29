import inspect

from importlib import import_module


def import_plugins(dotted_path: str) -> list[tuple[str, type]]:
    """
    Import all classes from the module specified by the dotted_path.
    If dotted_path is not a module, try importing it as a member of
    a module instead.

    returns: list of classes, or a list of a single class
    """
    try:
        module = import_module(dotted_path)
        return [(f"{dotted_path}.{name}", cls) for name, cls in inspect.getmembers(module, predicate=inspect.isclass)]
    except (ImportError, ModuleNotFoundError):
        try:
            module_path, class_name = dotted_path.rsplit(".", 1)
            module = import_module(module_path)
            return [(f"{module_path}.{class_name}", getattr(module, class_name))]
        except (ImportError, ModuleNotFoundError, AttributeError) as err:
            raise ImportError(f"'{dotted_path}' doesn't look like a module or class, or it has errors") from err
