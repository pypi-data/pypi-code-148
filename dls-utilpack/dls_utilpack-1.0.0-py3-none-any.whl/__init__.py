from importlib.metadata import version

__version__ = version("dls-utilpack")
del version

__all__ = ["__version__"]
