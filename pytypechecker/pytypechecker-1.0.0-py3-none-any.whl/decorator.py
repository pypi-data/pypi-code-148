from .Typecheck import Typecheck


def typecheck(func: callable) -> None:
    """Decorator used to enforce type-hints."""
    def decorated_function(*args, **kwargs) -> callable:
        Typecheck(func, *args, **kwargs)       
        result = func(*args, **kwargs)
        return result

    return decorated_function