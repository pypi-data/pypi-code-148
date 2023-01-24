"""Legacy :mod:`builtins` module."""
from __future__ import absolute_import

# Add temporary imports.
import sys as __sys

# Import `builtins` members.
try:
    from builtins import *
    from builtins import __doc__
except ImportError:
    from __builtin__ import *
    from __builtin__ import __doc__
__all__ = sorted(__k for __k in globals().keys()
                 if not (__k.startswith("__") or __k.endswith("__")))

# Start with backports.
if __sys.version_info[:2] < (3, 2):

    # Backport info:
    # - Python 3.2: first appeareance.
    class ResourceWarning(Warning):
        """Base class for warnings about resource usage."""

    if "ResourceWarning" not in __all__:
        __all__.append("ResourceWarning")

if (3, 0) <= __sys.version_info[:2] < (3, 2):

    # Backport info:
    # - Python 3.0 and 3.1: removed from builtins.
    def callable(obj):
        """Return whether the object is callable (i.e., some kind of function).

        Note that classes are callable, as are instances of classes with a
        __call__() method."""

        return hasattr(obj, "__call__")

if (3, 0) <= __sys.version_info[:2]:

    # Backport info:
    # - Python 3: removed `basestring` type, useful for Python 2 compatibility.
    # pylint: disable=invalid-name
    __type = type
    class type(__type):
        """Temporary metaclass for the ported `basestring` type object."""

        def __instancecheck__(cls, instance):
            """check if an object is an instance"""
            return isinstance(instance, str)

        def __subclasscheck__(cls, subclass):
            """check if a class is a subclass"""
            return issubclass(subclass, str)

        def __setattr__(cls, name, value):
            msg = "can't set attributes of built-in/extension type '{0}'"
            raise TypeError(msg.format(cls.__name__))

        def mro(cls):
            """Return a type's method resolution order."""
            return [cls, object]

    __metabasestring, type = type, __type
    class basestring(object):
        """Type basestring cannot be instantiated; it is the base for str and unicode."""

        def __new__(cls, *args, **kwargs):
            del args, kwargs
            if not isinstance(cls, type):
                msg = "{0}.__new__(X): X is not a type object ({1})"
                raise TypeError(msg.format(basestring.__name__, type(cls).__name__))
            if cls == basestring:
                msg = "The basestring type cannot be instantiated"
                raise TypeError(msg)
            if issubclass(cls, str):
                msg = "{0}.__new__({1}) is not safe, use {1}.__new__()"
                raise TypeError(msg.format(basestring.__name__, cls.__name__))
            msg = "{0}.__new__({1}): {1} is not a subtype of {0}"
            raise TypeError(msg.format(basestring.__name__, cls.__name__))

    basestring = __metabasestring(
        basestring.__name__,
        basestring.__bases__,
        vars(basestring).copy())
    del __metabasestring

# Remove temporary imports.
del __sys
