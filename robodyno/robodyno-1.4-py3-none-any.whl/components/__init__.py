# from .motor import Motor
from .can_bus.can_bus_device import CanBusDevice
from .can_bus.motor import Motor
from ..interfaces import CanBus as __CanBus

import sys
if sys.version_info < (3, 10):
    from importlib_metadata import entry_points
else:
    from importlib.metadata import entry_points
__thismodule = sys.modules[__name__]

__components = {}

can_eps = entry_points(group='robodyno.components.can_bus')
for ep in can_eps:
    try:
        __components[ep.name].update({'can_bus': ep.load()})
    except:
        __components.update({ep.name: {'can_bus': ep.load()}})

try:
    from .webots.webots_device import WebotsDevice
    from .webots.motor import Motor
    from ..interfaces import Webots as __Webots

    wb_eps = entry_points(group='robodyno.components.webots')
    for ep in wb_eps:
        try:
            __components[ep.name].update({'webots': ep.load()})
        except:
            __components.update({ep.name: {'webots': ep.load()}})
except:
    __Webots = None

def get_iface_name(iface):
    if isinstance(iface, __CanBus):
        return 'can_bus'
    elif isinstance(iface, __Webots):
        return 'webots'
    else:
        return ''

def component_factory(cls_name):
    try:
        return lambda iface, *args, **kwargs: __components[cls_name][get_iface_name(iface)](iface, *args, **kwargs)
    except:
        raise TypeError('The Class is invalid with this interface.')

for component in __components:
    setattr(__thismodule, component, component_factory(component))