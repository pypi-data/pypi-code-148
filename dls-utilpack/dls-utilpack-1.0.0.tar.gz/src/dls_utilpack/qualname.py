# ----------------------------------------------------------------------------------------
def qualname(object):
    if hasattr(object, "__module__"):
        module = object.__module__ + "."
    else:
        module = ""

    if hasattr(object, "__qualname__"):
        qualname = object.__qualname__
    else:
        qualname = type(object).__name__

    return module + qualname
