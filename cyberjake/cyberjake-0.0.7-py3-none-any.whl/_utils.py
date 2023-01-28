""" Internal Utility functions"""
from functools import wraps

_INSTALLED_MODULES = {"discord.py": False, "requests": False, "packaging": False}


def _check_required_modules(module_name: str):
    """Checks if a required module is installed"""

    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not _INSTALLED_MODULES.get(module_name, False):
                raise ModuleNotFoundError(f"Need {module_name} module installed")
            return view_func(*args, **kwargs)

        return wrapper

    return decorator
