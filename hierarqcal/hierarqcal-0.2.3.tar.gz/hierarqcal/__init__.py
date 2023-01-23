from .core import Qconv, Qdense, Qpool, Qfree, Qcnn, Qmotifs, Qmotif
from .utils import plot_motifs, plot_motif

import importlib.util
import sys
def lazy_import(name):
    spec = importlib.util.find_spec(name)
    loader = importlib.util.LazyLoader(spec.loader)
    spec.loader = loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    loader.exec_module(module)
    return module

cirq = lazy_import("cirq")

__all__ = [
    "Qcnn",
    "Qconv",
    "Qdense",
    "Qpool",
    "Qfree",
    "Qmotif",
    "Qmotifs",
    "plot_motifs",
    "plot_motif",
    "cirq",
]