#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .print_2 import print
from .write_2 import write
class histogram(Group):
    """
    'histogram' child.
    """

    fluent_name = "histogram"

    command_names = \
        ['print', 'write']

    print: print = print
    """
    print command of histogram.
    """
    write: write = write
    """
    write command of histogram.
    """
