#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""webots_device.py
Time    :   2023/01/05
Author  :   song 
Version :   1.0
Contact :   zhaosongy@126.com
License :   (C)Copyright 2022, robottime / robodyno

Webots device node base class.
"""

from enum import Enum
from robodyno.interfaces import Webots

class WebotsDevice(object):
    """Webots common device node."""

    class DeviceType(Enum):
        """Robodyno device type and uuid pairs."""
        ROBODYNO_PRO_44 = 0x00
        ROBODYNO_PRO_12 = 0x01
        ROBODYNO_PRO_50  = 0x02
        ROBODYNO_PRO_100 = 0x03
        ROBODYNO_PRO_DIRECT = 0x0F
        ROBODYNO_PLUS_50  = 0x10
        ROBODYNO_PLUS_100 = 0x11
        ROBODYNO_PLUS_12  = 0x12
        ROBODYNO_PLUS_DIRECT = 0x1F
        ROBODYNO_EXB_FCTY = 0x80
        ROBODYNO_THIRD_PARTY = 0xA0

        @classmethod
        def _missing_(cls, value):
            return cls.ROBODYNO_THIRD_PARTY
    
    def __init__(self, iface, id = 0x10, type = 'ROBODYNO_THIRD_PARTY', auto_register = True):
        """Init node with webots interface and id.
        
        Args:
            iface: webots interface
            id: node id
            type: robodyno device type name
            auto_register: auto register self to webots interface
        """
        try:
            self.name = '0x{:02X}'.format(id)
        except:
            self.name = id
        if not isinstance(iface, Webots):
            raise ValueError('Use a webots interface to init a webots device.')
        
        self.type = self.DeviceType[type]
        self._iface = iface
        if auto_register:
            iface.register(self)
    
    def __del__(self):
        """Collect node from memory."""
        self._iface.deregister(self)
    
    def get_version(self):
        """Get device simulation version.
        
        Returns:
            dictionary of device version
        """
        return {
            'main_version': 4,
            'sub_version': 0,
            'type': self.type
        }

    def update(self):
        """Simulation update callback."""
        pass