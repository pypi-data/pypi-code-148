from importlib.metadata import version

__version__ = version("test_release_workflow")
del version

def some_dumb_change():
    print("Hi")