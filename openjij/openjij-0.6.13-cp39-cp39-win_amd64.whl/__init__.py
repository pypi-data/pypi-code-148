

""""""# start delvewheel patch
def _delvewheel_init_patch_1_2_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'openjij.libs'))
    is_pyinstaller = getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if not is_pyinstaller or os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-openjij-0.6.13')
        if not is_pyinstaller or os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-openjij-0.6.13')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if not is_pyinstaller or os.path.isfile(lib_path):
                    ctypes.WinDLL(lib_path)


_delvewheel_init_patch_1_2_0()
del _delvewheel_init_patch_1_2_0
# end delvewheel patch

from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)

from openjij import cxxjij

from openjij.model.model import BinaryPolynomialModel, BinaryQuadraticModel
from openjij.sampler.csqa_sampler import CSQASampler
from openjij.sampler.response import Response
from openjij.sampler.sa_sampler import SASampler
from openjij.sampler.sqa_sampler import SQASampler
from openjij.utils.benchmark import solver_benchmark
from openjij.utils.res_convertor import convert_response
from openjij.variable_type import BINARY, SPIN, Vartype, cast_vartype

__all__ = [
    "cxxjij",
    "SPIN",
    "BINARY",
    "Vartype",
    "cast_vartype",
    "Response",
    "SASampler",
    "SQASampler",
    "CSQASampler",
    "BinaryQuadraticModel",
    "BinaryPolynomialModel",
    "solver_benchmark",
    "convert_response",
]
