#
# This is an auto-generated file.  DO NOT EDIT!
#

from ansys.fluent.core.solver.flobject import *

from ansys.fluent.core.solver.flobject import _ChildNamedObjectAccessorMixin

from ansys.fluent.core.solver.flobject import _CreatableNamedObjectMixin

from ansys.fluent.core.solver.flobject import _NonCreatableNamedObjectMixin

from .ambient_color import ambient_color
from .headlight_setting import headlight_setting
from .lights_on import lights_on
from .lighting_interpolation import lighting_interpolation
from .set_light import set_light
class lights(Group):
    """
    'lights' child.
    """

    fluent_name = "lights"

    child_names = \
        ['ambient_color', 'headlight_setting', 'lights_on',
         'lighting_interpolation']

    ambient_color: ambient_color = ambient_color
    """
    ambient_color child of lights.
    """
    headlight_setting: headlight_setting = headlight_setting
    """
    headlight_setting child of lights.
    """
    lights_on: lights_on = lights_on
    """
    lights_on child of lights.
    """
    lighting_interpolation: lighting_interpolation = lighting_interpolation
    """
    lighting_interpolation child of lights.
    """
    command_names = \
        ['set_light']

    set_light: set_light = set_light
    """
    set_light command of lights.
    """
