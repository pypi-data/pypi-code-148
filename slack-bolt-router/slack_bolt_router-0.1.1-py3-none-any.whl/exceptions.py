"""
Contains all Exception classes that can be raised in slack-bolt-router package.

(c) Dmytro Hoi <code@dmytrohoi.com>, 2021 | MIT License
"""
__all__ = (
    "InvalidRouteTypeNameError",
)


class InvalidRouteTypeNameError(Exception):
    """Invalid the route type name passed to Router."""
    pass
