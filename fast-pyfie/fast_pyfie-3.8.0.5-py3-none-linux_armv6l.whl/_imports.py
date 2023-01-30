_ENABLE_NUMPY = False
try:
    import numpy
except ImportError:
    _ENABLE_NUMPY = False
else:
    _ENABLE_NUMPY = True

_ENABLE_PYPLOT = False
try:
    import matplotlib.pyplot
except ImportError:
    _ENABLE_PYPLOT = False
else:
    _ENABLE_PYPLOT = True

# def _raise_if_numpy_unavailable():
#     if not _ENABLE_NUMPY:
#         raise ImportError("Failed to import numpy module")


def _raise_if_pyplot_unavailable():
    if not _ENABLE_PYPLOT:
        raise ImportError("Failed to import matplotlib.pyplot module")
