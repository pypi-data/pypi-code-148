#!/usr/bin/env python
# -*-coding:utf-8 -*-
"""can_bus_device.py
Time    :   2023/01/02
Author  :   song 
Version :   1.0
Contact :   zhaosongy@126.com
License :   (C)Copyright 2022, robottime / robodyno

Can bus device base class.
"""

from enum import Enum
from robodyno.interfaces import CanBus

class CanBusDevice(object):
    """Can bus robodyno common device node."""
    
    CMD_GET_VERSION = 0x01

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
        ROBODYNO_GENERAL_GRIPPER = 0x61
        ROBODYNO_STEPPER_DRIVER = 0x62
        ROBODYNO_VACUUM_GRIPPER = 0x63
        ROBODYNO_ADAPTIVE_GRIPPER = 0x64
        ROBODYNO_FLEXIBLE_GRIPPER = 0x65
        ROBODYNO_EXB_FCTY = 0x80
        ROBODYNO_THIRD_PARTY = 0xFF

        @classmethod
        def _missing_(cls, value):
            return cls.ROBODYNO_THIRD_PARTY

    def __init__(self, iface, id = 0x10):
        """Init device with interface and id
        
        Args:
            iface: can bus interface
            id: device id
        """
        if id < 0x01 or id >= 0x40:
            raise ValueError('Use a valid device id range from 0x01 to 0x40.')
        if not isinstance(iface, CanBus):
            raise ValueError('Use a can bus interface to init a can bus device.')
        self._iface = iface
        self.id = id
        self.fw_ver = None
        self.type = self.DeviceType.ROBODYNO_THIRD_PARTY
    
    @CanBus.get_from_bus(CMD_GET_VERSION, '<HHI')
    def get_version(self, main_ver, sub_ver, type):
        """Get device firmware version.
        
        Args:
            timeout: 0 indicates unlimited timeout(s)
        
        Returns:
            dictionary of device version
            None if timeout
        """
        self.fw_ver = float('{}.{}'.format(main_ver, sub_ver))
        self.type = self.DeviceType(type)
        return {
            'main_version': main_ver,
            'sub_version': sub_ver,
            'type': self.DeviceType(type)
        }
