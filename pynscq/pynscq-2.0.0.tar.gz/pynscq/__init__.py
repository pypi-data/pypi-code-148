#
# Copyright 2021-2023 NVIDIA Corporation.  All rights reserved.
#
# NOTICE TO USER:
#
# This source code is subject to NVIDIA ownership rights under U.S. and
# international Copyright laws.  Users and possessors of this source code
# are hereby granted a nonexclusive, royalty-free license to use this code
# in individual and commercial software.
#
# NVIDIA MAKES NO REPRESENTATION ABOUT THE SUITABILITY OF THIS SOURCE
# CODE FOR ANY PURPOSE.  IT IS PROVIDED "AS IS" WITHOUT EXPRESS OR
# IMPLIED WARRANTY OF ANY KIND.  NVIDIA DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOURCE CODE, INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY, NONINFRINGEMENT, AND FITNESS FOR A PARTICULAR PURPOSE.
# IN NO EVENT SHALL NVIDIA BE LIABLE FOR ANY SPECIAL, INDIRECT, INCIDENTAL,
# OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS,  WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION,  ARISING OUT OF OR IN CONNECTION WITH THE USE
# OR PERFORMANCE OF THIS SOURCE CODE.
#
# U.S. Government End Users.   This source code is a "commercial item" as
# that term is defined at  48 C.F.R. 2.101 (OCT 1995), consisting  of
# "commercial computer  software"  and "commercial computer software
# documentation" as such terms are  used in 48 C.F.R. 12.212 (SEPT 1995)
# and is provided to the U.S. Government only as a commercial end item.
# Consistent with 48 C.F.R.12.212 and 48 C.F.R. 227.7202-1 through
# 227.7202-4 (JUNE 1995), all U.S. Government End Users acquire the
# source code with only those rights set forth herein.
#
# Any use of this source code in individual and commercial software must
# include, in the user documentation and internal comments to the code,
# the above Disclaimer and U.S. Government End Users Notice.
#

import ctypes
from ctypes.util import find_library
from warnings import warn


nscq_api_version = [2,0,0]

################################################################
#####                                                      #####
#####               Internal Helper Classes                #####
#####                                                      #####
################################################################

class _Constants(object):
    """
    Helper class to quickly allow for converting a value to it's associated
    attribute.
    """
    @classmethod
    def toString(cls, value):
        if isinstance(value, nscq_rc_t):
            value = value.value
        if not isinstance(value, int):
            raise TypeError("value must be of type int, not %s" % type(value))
        for key in [keys for keys in dir(cls) if not keys.startswith('__')]:
            try:
                if cls.__dict__[key] == value:
                    return key
            except KeyError as e:
                break
        raise AttributeError("%s has no match for %d" %(cls.__name__, value))

    def __new__(cls, value):
        return cls.toString(value)


class _PrintableStructure(ctypes.Structure):
    """
    Abstract class that produces nicer __str__ output than ctypes.Structure.
    e.g. instead of:
      >>> print str(obj)
      <class_name object at 0x7fdf82fef9e0>
    this class will print
      class_name(field_name: formatted_value, field_name: formatted_value)

    _fmt_ dictionary of <str _field_ name> -> <str format>
    e.g. class that has _field_ 'hex_value', c_uint could be formatted with
      _fmt_ = {"hex_value" : "%08X"}
    to produce nicer output.
    Default fomratting string for all fields can be set with key "<default>" like:
      _fmt_ = {"<default>" : "%d MHz"} # e.g all values are numbers in MHz.
    If not set it's assumed to be just "%s"

    Exact format of returned str from this class is subject to change in the future.
    """
    _fmt_ = {}
    def __str__(self):
        result = []
        for x in self._fields_:
            key = x[0]
            value = getattr(self, key)
            fmt = "%s"
            if key in self._fmt_:
                fmt = self._fmt_[key]
            elif "<default>" in self._fmt_:
                fmt = self._fmt_["<default>"]
            result.append(("%s: " + fmt) % (key, value))
        return self.__class__.__name__ + "(" +  ", ".join(result) + ")"
    __repr__ = __str__

################################################################
#####                                                      #####
#####                      Constants                       #####
#####                                                      #####
################################################################


class nscq_rcs(_Constants):
    NSCQ_RC_SUCCESS                      = 0
    NSCQ_RC_WARNING_RDT_INIT_FAILURE     = 1
    NSCQ_RC_ERROR_NOT_IMPLEMENTED        = -1
    NSCQ_RC_ERROR_INVALID_UUID           = -2
    NSCQ_RC_ERROR_RESOURCE_NOT_MOUNTABLE = -3
    NSCQ_RC_ERROR_OVERFLOW               = -4
    NSCQ_RC_ERROR_UNEXPECTED_VALUE       = -5
    NSCQ_RC_ERROR_UNSUPPORTED_DRV        = -6
    NSCQ_RC_ERROR_DRV                    = -7
    NSCQ_RC_ERROR_TIMEOUT                = -8
    NSCQ_RC_ERROR_EXT                    = -127
    NSCQ_RC_ERROR_UNSPECIFIED            = -128
class nscq_rc_t(ctypes.c_int8):
    pass


class nscq_driver_fabric_states(_Constants):
    NSCQ_DRIVER_FABRIC_STATE_UNKNOWN         = -1
    NSCQ_DRIVER_FABRIC_STATE_OFFLINE         = 0
    NSCQ_DRIVER_FABRIC_STATE_STANDBY         = 1
    NSCQ_DRIVER_FABRIC_STATE_CONFIGURED      = 2
    NSCQ_DRIVER_FABRIC_STATE_MANAGER_TIMEOUT = 3
    NSCQ_DRIVER_FABRIC_STATE_MANAGER_ERROR   = 4
    NSCQ_DRIVER_FABRIC_STATE_MANAGER_SLEEP   = 5


class nscq_device_fabric_states(_Constants):
    NSCQ_DEVICE_FABRIC_STATE_UNKNOWN     = -1
    NSCQ_DEVICE_FABRIC_STATE_OFFLINE     = 0
    NSCQ_DEVICE_FABRIC_STATE_STANDBY     = 1
    NSCQ_DEVICE_FABRIC_STATE_CONFIGURED  = 2
    NSCQ_DEVICE_FABRIC_STATE_BLACKLISTED = 3


class nscq_nvlink_states(_Constants):
    NSCQ_NVLINK_STATE_UNKNOWN  = -1
    NSCQ_NVLINK_STATE_OFF      = 0
    NSCQ_NVLINK_STATE_SAFE     = 1
    NSCQ_NVLINK_STATE_ACTIVE   = 2
    NSCQ_NVLINK_STATE_ERROR    = 3
class nscq_nvlink_state_t(ctypes.c_int8):
    pass


class nscq_device_blacklist_reasons(_Constants):
    NSCQ_DEVICE_BLACKLIST_REASON_UNKNOWN                     = -1
    NSCQ_DEVICE_BLACKLIST_REASON_NONE                        = 0
    NSCQ_DEVICE_BLACKLIST_REASON_MANUAL_OUT_OF_BAND          = 1
    NSCQ_DEVICE_BLACKLIST_REASON_MANUAL_IN_BAND              = 2
    NSCQ_DEVICE_BLACKLIST_REASON_MANUAL_PEER                 = 3
    NSCQ_DEVICE_BLACKLIST_REASON_TRUNK_LINK_FAILURE          = 4
    NSCQ_DEVICE_BLACKLIST_REASON_TRUNK_LINK_FAILURE_PEER     = 5
    NSCQ_DEVICE_BLACKLIST_REASON_ACCESS_LINK_FAILURE         = 6
    NSCQ_DEVICE_BLACKLIST_REASON_ACCESS_LINK_FAILURE_PEER    = 7
    NSCQ_DEVICE_BLACKLIST_REASON_UNSPEC_DEVICE_FAILURE       = 8
    NSCQ_DEVICE_BLACKLIST_REASON_UNSPEC_DEVICE_FAILURE_PEER  = 9
class nscq_nvlink_blacklist_reason_t(ctypes.c_int8):
    pass

class nscq_arch(_Constants):
    NSCQ_ARCH_SV10 = 0
    NSCQ_ARCH_LR10 = 1
    NSCQ_ARCH_LS10 = 2
class nscq_arch_t(ctypes.c_int8):
    pass

class nscq_nvlink_rx_sublink_states(_Constants):
    NSCQ_NVLINK_STATUS_SUBLINK_RX_STATE_UNKNOWN      = -1
    NSCQ_NVLINK_STATUS_SUBLINK_RX_STATE_HIGH_SPEED_1 = 0
    NSCQ_NVLINK_STATUS_SUBLINK_RX_STATE_SINGLE_LANE  = 1
    NSCQ_NVLINK_STATUS_SUBLINK_RX_STATE_TRAINING     = 2
    NSCQ_NVLINK_STATUS_SUBLINK_RX_STATE_SAFE_MODE    = 3
    NSCQ_NVLINK_STATUS_SUBLINK_RX_STATE_OFF          = 4
class nscq_nvlink_rx_sublink_state_t(ctypes.c_int8):
    pass

class nscq_nvlink_tx_sublink_states(_Constants):
    NSCQ_NVLINK_STATUS_SUBLINK_TX_STATE_UNKNOWN      = -1
    NSCQ_NVLINK_STATUS_SUBLINK_TX_STATE_HIGH_SPEED_1 = 0
    NSCQ_NVLINK_STATUS_SUBLINK_TX_STATE_SINGLE_LANE  = 1
    NSCQ_NVLINK_STATUS_SUBLINK_TX_STATE_TRAINING     = 2
    NSCQ_NVLINK_STATUS_SUBLINK_TX_STATE_SAFE_MODE    = 3
    NSCQ_NVLINK_STATUS_SUBLINK_TX_STATE_OFF          = 4
class nscq_nvlink_tx_sublink_state_t(ctypes.c_int8):
    pass

NSCQ_SESSION_CREATE_MOUNT_DEVICES = 1
NSCQ_SESSION_PATH_REGISTER_OBSERVER_WATCH = 1

################################################################
#####                                                      #####
#####                 Anonymous Structures                 #####
#####                                                      #####
################################################################


class nscq_session_st(_PrintableStructure):
    pass
nscq_session_t = ctypes.POINTER(nscq_session_st)


class nscq_observer_st(_PrintableStructure):
    pass
nscq_observer_t = ctypes.POINTER(nscq_observer_st)



################################################################
#####                                                      #####
#####                       Structures                     #####
#####                                                      #####
################################################################

class nscq_uuid_t(_PrintableStructure):
    _fields_ = [("bytes", ctypes.c_uint8 * 16)]

    def __str__(self):
        return "[%s]" % (", ".join(hex(x) for x in self.bytes))

    __repr__ = __str__


p_nscq_uuid_t = ctypes.POINTER(nscq_uuid_t)


class nscq_fabric_state_t(_PrintableStructure):
    _fields_ = [
        ("driver", ctypes.c_uint16),
        ("device", ctypes.c_uint16)
    ]


class nscq_pcie_location_t(_PrintableStructure):
    _fields_ = [
        ("domain", ctypes.c_uint32),
        ("bus", ctypes.c_uint8),
        ("device", ctypes.c_uint8),
        ("function", ctypes.c_uint8),
    ]


class nscq_label_t(_PrintableStructure):
    _fields_ = [("data", ctypes.c_char * 64)]

    def __str__(self):
        return self.data.decode("UTF-8")

    def __repr__(self):
        return self.__class__.__name__ + "(" + self.__str__() + ")"


class nscq_link_caps_t(_PrintableStructure):
    _fields_ = [
        ("protocol_version", ctypes.c_uint8),
        ("link_width", ctypes.c_uint8),
        ("bandwidth", ctypes.c_uint32),
    ]


class nscq_link_throughput_t(_PrintableStructure):
    """
    All in Mib
    """

    _fields_ = [
        ("rx", ctypes.c_uint64),
        ("tx", ctypes.c_uint64)
    ]
    _fmt_ = [("<default>", "%d Mib")]


class nscq_error_t(_PrintableStructure):
    _fields_ = [
        ("error_value", ctypes.c_uint32),
        ("time", ctypes.c_uint64)
    ]

class nscq_link_max_correctable_error_rate_t(_PrintableStructure):
    _fields_ = [
        ("last_updated", ctypes.c_uint32),
        ("errors_per_minute", ctypes.c_uint32)
    ]

class nscq_link_error_t(_PrintableStructure):
    _fields_ = [
        ("instance", ctypes.c_uint8),
        ("error", ctypes.c_uint32),
        ("timestamp", ctypes.c_uint32),
        ("count", ctypes.c_uint64)
    ]

class nscq_ecc_error_count_t(_PrintableStructure):
    _fields_ = [
        ("uncorrected_total", ctypes.c_uint64),
        ("corrected_total", ctypes.c_uint64),
        ("error_count", ctypes.c_uint32)
    ]

class nscq_ecc_error_entry_t(_PrintableStructure):
    _fields_ = [
        ("sxid", ctypes.c_uint32),
        ("link_id", ctypes.c_uint8),
        ("timestamp", ctypes.c_uint32),
        ("address_valid", ctypes.c_uint8),
        ("address", ctypes.c_uint32),
        ("corrected_count", ctypes.c_uint32),
        ("uncorrected_count", ctypes.c_uint32)
    ]

class nscq_sxid_error_entry_t(_PrintableStructure):
    _fields_ = [
        ("sxid", ctypes.c_uint32),
        ("timestamp", ctypes.c_uint32)
    ]

class nscq_vc_latency_t(_PrintableStructure):
    _fields_ = [
        ("low", ctypes.c_uint64),
        ("medium", ctypes.c_uint64),
        ("high", ctypes.c_uint64),
        ("panic", ctypes.c_uint64),
        ("count", ctypes.c_uint64)
    ]

class nscq_nvlink_clock_info_t(_PrintableStructure):
    _fields_ = [
        ("freq_khz", ctypes.c_uint32),
        ("vcofreq_khz", ctypes.c_uint32),
    ]

class nscq_nvlink_voltage_info_t(_PrintableStructure):
     _fields_ = [
        ("voltage_mvolt", ctypes.c_uint32),
    ]

class nscq_nvlink_current_info_t(_PrintableStructure):
    _fields_ = [
        ("iddq", ctypes.c_uint32),
        ("iddq_rev", ctypes.c_uint32),
        ("iddq_dvdd", ctypes.c_uint32),
    ]

class nscq_cci_raw_cmis_presence_t(_PrintableStructure):
    _fields_ = [
        ("cages_mask", ctypes.c_uint32),
        ("modules_mask", ctypes.c_uint32),
    ]

class nscq_cci_raw_cmis_lane_mapping_t(_PrintableStructure):
    _fields_ = [
        ("link_mask", ctypes.c_uint64),
        ("encoded_value", ctypes.c_uint64),
    ]

class nscq_cci_raw_cmis_read_t(_PrintableStructure):
    _fields_ = [("data", ctypes.c_uint8 * 128)]

# port[i] indicates nvswitch_port that occupies osfp lane i
# Port value starts from 0. 0xFF value indicates no port.
class nscq_cci_osfp_lane_mapping_t(_PrintableStructure):
    _fields_ = [("port", ctypes.c_uint8 * 8)]

class nscq_cci_osfp_str_t(_PrintableStructure):
    _fields_ = [("data", ctypes.c_uint8 * 16)]

class nscq_cci_osfp_lane_monitor_t(_PrintableStructure):
    _fields_ = [
        ("tx_power", ctypes.c_uint32 * 8),
        ("rx_power", ctypes.c_uint32 * 8),
        ("tx_bias", ctypes.c_uint32 * 8),
    ]

class nscq_cci_osfp_module_monitor_t(_PrintableStructure):
    _fields_ = [
        ("temperature", ctypes.c_int16),
        ("supply_volt", ctypes.c_uint32),
    ]

class nscq_cci_osfp_module_firmware_version_t(_PrintableStructure):
    _fields_ = [
        ("major_rev", ctypes.c_uint8),
        ("minor_rev", ctypes.c_uint8),
    ]

class nscq_cci_osfp_signal_integrity_t(_PrintableStructure):
    _fields_ = [
        ("tx_input_eq", ctypes.c_uint8 * 8),
        ("rx_output_pre_cursor", ctypes.c_uint8 * 8),
        ("rx_output_post_cursor", ctypes.c_uint8 * 8),
    ]

class nscq_cci_osfp_data_path_state_t(_PrintableStructure):
    _fields_ = [
        ("state", ctypes.c_uint8 * 8),
    ]

class nscq_temperature_sensors_t(_PrintableStructure):
    _fields_ = [
        ("sensors", ctypes.c_int32 * 16),
        ("num_sensor", ctypes.c_uint8),
    ]

class nscq_drv_version_t(_PrintableStructure):
    """Not actually defined in the header file.
    Helps with unpacking the drv version.
    """

    _fields_ = [
        ("patch", ctypes.c_uint32, 12),
        ("minor", ctypes.c_uint32, 12),
        ("major", ctypes.c_uint32, 8),
    ]



"""
This is the macro that builds nscq_{}_result_t

#define _NSCQ_RESULT_TYPE(t, m) \
    typedef struct {            \
        nscq_rc_t rc;           \
        t m;                    \
    } nscq_##m##_result_t

The structures below are the ones that are defined
"""


class nscq_session_result_t(_PrintableStructure):
    _fields_ = [("rc", nscq_rc_t), ("session", nscq_session_t)]


class nscq_observer_result_t(_PrintableStructure):
    _fields_ = [("rc", nscq_rc_t), ("observer", nscq_observer_t)]


################################################################
#####                                                      #####
#####                   Internal Functions                 #####
#####                                                      #####
################################################################


_nscqlib = None
def _loadNscq():
    global _nscqlib
    library = find_library("nvidia-nscq")
    if _nscqlib is None:
        try:
            _nscqlib = ctypes.CDLL(library)
        except OSError as error:
            raise error
_loadNscq()

__FCACHE = {}
def __nscqFindFunc(name, restype=None):
    global __FCACHE
    if name in __FCACHE:
        return __FCACHE[name]
    fn = getattr(_nscqlib, name)
    fn.restype = restype
    __FCACHE[name] = fn
    return fn


class NSCQResult:
    """NSCQ Result

    Class for handling return codes:
    * -128 to -1 = error
    * 0          = success
    * 1 to 127   = warning
    """

    def __init__(self, rc=None, message=None):
        super().__init__()
        self.rc = rc
        self.name = nscq_rcs.toString(rc)
        self.message = message if message else self.name

    def __str__(self):
        return self.message


class NSCQWarning(NSCQResult, UserWarning):
    """NSCQ Warning

    For return codes between 1 and 127.
    """

    pass


class NSCQError(NSCQResult, Exception):
    """NSCQ Error

    For return codes between -128 and -1
    """

    pass


def nscq_handle_rc(rc):
    if isinstance(rc, nscq_rc_t):
        value = rc.value
    elif isinstance(rc, int):
        value = rc
    else:
        raise TypeError(
            "rc must be of type int or nscq_rc_t, got type: " + str(type(rc))
        )
    if value < nscq_rcs.NSCQ_RC_SUCCESS:
        raise NSCQError(value)
    elif value > nscq_rcs.NSCQ_RC_SUCCESS:
        warn(NSCQWarning(value), stacklevel=3)



################################################################
#####                                                      #####
#####                       Functions                      #####
#####                                                      #####
################################################################


def nscq_uuid_to_label(uuid: nscq_uuid_t, flags=0):
    """returns nscq_label_t"""
    if not isinstance(uuid, nscq_uuid_t):
        raise TypeError("Uuid must be of type nscq_uuid_t")
    fn = __nscqFindFunc("nscq_uuid_to_label", restype=nscq_rc_t)
    label = nscq_label_t()
    res = fn(ctypes.byref(uuid), ctypes.byref(label), ctypes.c_uint32(flags))
    nscq_handle_rc(res)
    return label


def nscq_session_create(flags=0):
    """return nscq_session_t"""
    fn = __nscqFindFunc("nscq_session_create", restype=nscq_session_result_t)
    res = fn(ctypes.c_uint32(flags))
    nscq_handle_rc(res.rc)
    return res.session


def nscq_session_destroy(session: nscq_session_t):
    if not isinstance(session, nscq_session_t):
        raise TypeError("Session must be of type nscq_session_t")
    fn = __nscqFindFunc("nscq_session_destroy")
    fn(session)


def nscq_session_mount(session: nscq_session_t, uuid: nscq_uuid_t, flags=0):
    """return nscq_rc_t (can be ignored)"""
    if not isinstance(session, nscq_session_t):
        raise TypeError("session must be of type nscq_session_t")
    if not isinstance(uuid, nscq_uuid_t):
        raise TypeError("uuid must be of type nscq_uuid_t, got type %s" % (type(uuid)))
    fn = __nscqFindFunc("nscq_session_mount", restype=nscq_rc_t)
    res = fn(session, ctypes.byref(uuid), ctypes.c_uint32(flags))
    nscq_handle_rc(res)
    return res


def nscq_session_unmount(session: nscq_session_t, uuid: nscq_uuid_t):
    if not isinstance(session, nscq_session_t):
        raise TypeError("session must be of type nscq_session_t")
    if not isinstance(uuid, nscq_uuid_t):
        raise TypeError("uuid must be of type nscq_uuid_t")
    fn = __nscqFindFunc("nscq_session_unmount")
    fn(session, uuid)


def nscq_session_path_observe(
    session: nscq_session_t, path: bytes, callback, user_data=None, flags=0
):
    """return nscq_rc_t (can be ignored)

    path should be a byte array, not a regular string
    callback needs to follow a set of rules, use @nscqCallback to create
    user_data should be a python object or None
    """

    if not isinstance(session, nscq_session_t):
        raise TypeError("session must be of type nscq_session_t")
    if not isinstance(path, bytes):
        raise TypeError(
            "path must be a byte array, please use provided paths unless you know what you're doing"
        )
    if not isinstance(callback, ctypes._CFuncPtr):
        raise TypeError(
            "Callback must be a CFUNCTYPE with correct values. Use the Helper Decorator"
        )
    fn = __nscqFindFunc("nscq_session_path_observe", restype=nscq_rc_t)
    res = fn(
        session,
        ctypes.c_char_p(path),
        callback,
        ctypes.pointer(ctypes.py_object(user_data)),
        ctypes.c_uint32(flags),
    )
    nscq_handle_rc(res)
    return res


def nscq_session_path_register_observer(
    session: nscq_session_t, path: bytes, callback, user_data, flags=0
):
    """return nscq_observer_t

    path should be a byte array, not a regular string
    callback needs to follow a set of rules, use @nscqCallback to create
    user_data should be a python object or None
    """
    if not isinstance(session, nscq_session_t):
        raise TypeError("session must be of type nscq_session_t")
    if not isinstance(path, bytes):
        raise TypeError(
            "path must be a string, please use provided paths unless you know what you're doing"
        )
    if not isinstance(callback, ctypes._CFuncPtr):
        raise TypeError(
            "Callback must be a CFUNCTYPE with correct values. Use the Helper Decorator"
        )
    fn = __nscqFindFunc(
        "nscq_session_path_register_observer", restype=nscq_observer_result_t
    )
    res = fn(
        session,
        ctypes.c_char_p(path),
        callback,
        ctypes.pointer(ctypes.py_object(user_data)),
        ctypes.c_uint32(flags),
    )
    nscq_handle_rc(res.rc)
    return res.observer


def nscq_observer_deregister(observer: nscq_observer_t):
    if not isinstance(observer, nscq_observer_t):
        raise TypeError("Observer must be type nscq_observer_t")
    fn = __nscqFindFunc("nscq_observer_deregister")
    fn(observer)


def nscq_observer_observe(observer: nscq_observer_t, flags=0):
    """return nscq_rc_t (can be ignored)"""
    if not isinstance(observer, nscq_observer_t):
        raise TypeError("Observer must be of type nscq_observer_t")
    fn = __nscqFindFunc("nscq_observer_observe", restype=nscq_rc_t)
    res = fn(observer, ctypes.c_uint32(flags))
    nscq_handle_rc(res)
    return res


def nscq_session_observe(session: nscq_session_t, flags=0):
    """return nscq_rc_t (can be ignored)"""
    if not isinstance(session, nscq_session_t):
        raise TypeError("session must be of type nscq_session_t")
    fn = __nscqFindFunc("nscq_session_observe", restype=nscq_rc_t)
    res = fn(session, ctypes.c_uint32(flags))
    nscq_handle_rc(res)
    return res


def nscq_session_watch(session: nscq_session_t, timeout, flags=0):
    """return nscq_rc_t (can be ignored)"""
    if not isinstance(session, nscq_session_t):
        raise TypeError("session must be of type nscq_session_t")
    fn = __nscqFindFunc("nscq_session_watch", restype=nscq_rc_t)
    res = fn(session, ctypes.c_uint32(flags), ctypes.c_uint32(timeout))
    nscq_handle_rc(res)
    return res


################################################################
#####                                                      #####
#####                     Helpers                          #####
#####                                                      #####
################################################################


user_data_type = ctypes.POINTER(ctypes.py_object)
def user_data_unwrap(user_data):
    """returns a python object

    If a callback is created with @nscqCallback, and the user_data type is
    defined with user_data_type, this helper function can be used to extract the
    origional python object.
    """
    if isinstance(user_data, user_data_type):
        return user_data.contents.value


class NSCQSession:
    """A Helper class to handle creating, destroying, and keeping track of a session.

    example:

    with NSCQSession() as session:
        session.path_observe(b"/drv/nvswitch/version", drv_version_callback)
    """

    def __init__(self, flags=0, uuids=None):
        self.session = nscq_session_create(flags)
        if uuids:
            uuids = uuids if isinstance(uuids, list) else list(uuids)
            for uuid in uuids:
                nscq_session_mount(self.session, uuid, flags)

    def __enter__(self):
        return self

    def __exit__(self, _type, _value, _traceback):
        nscq_session_destroy(self.session)

    def mount(self, uuid: nscq_uuid_t, flags=0):
        return nscq_session_mount(self.session, uuid, flags)

    def unmount(self, uuid: nscq_uuid_t):
        nscq_session_unmount(self.session, uuid)

    def path_observe(self, path: bytes, callback, user_data=None, flags=0):
        return nscq_session_path_observe(self.session, path, callback, user_data, flags)

    def path_register_observer(self, path: bytes, callback, user_data=None, flags=0):
        return nscq_session_path_register_observer(
            self.session, path, callback, user_data, flags
        )

    def observe(self, flags=0):
        return nscq_session_observe(self.session, flags)

    def watch(self, timeout, flags=0):
        return nscq_session_watch(self.session, timeout, flags)

__nscqVariables = [var for var in dir() if var.endswith("_t")]
__nscqCtypes = [
    var.__name__
    for var in [
        ctypes.c_uint8,
        ctypes.c_int16,
        ctypes.c_uint16,
        ctypes.c_uint32,
        ctypes.c_uint64,
        ctypes.c_void_p,
        p_nscq_uuid_t,
        user_data_type,
        ctypes.c_bool,
    ]
]

def nscqCallback(*callback_arguments, **kwargs):
    """decorator to create callbacks for observers.
    Checks argument types to ensure that all are valid nscq types and are expected to be returned.

    This is just a wrapper around ctypes.CFUNCTYPE. kwargs are passed through.

    All callbacks will end with three variables:
      the return code: nscq_rc_t
      the result of the query: variable type
      the user_data: either a void* or user_data_type

    The first few arguments can vary, but usually will follow the pattern: p_nscq_uuid_t (nscq_uuid_t*), uint32, uint32
    These are typically Device, Port, and Lane, depending on what the callback returns.
    """
    if len(callback_arguments) < 3:
        raise TypeError(
            "Callbacks take a minimum of three arguments. %d provided"
            % (len(callback_arguments))
        )
    for argnum in range(len(callback_arguments)):
        arg = callback_arguments[argnum]
        if arg.__name__ not in __nscqVariables + __nscqCtypes:
            raise TypeError(
                "Argument %d (%s) not a valid callback argument."
                % (argnum + 1, str(arg))
            )
    if not callback_arguments[-1] in [ctypes.c_void_p, user_data_type]:
        raise TypeError(
            "The user_data argument must be passed as a void* or user_data_type"
        )
    if callback_arguments[-3] != nscq_rc_t:
        raise TypeError(
            "the return_code argument must be of type nscq_rc_t, got type %s"
            % (callback_arguments[-3])
        )
    return ctypes.CFUNCTYPE(None, *callback_arguments, **kwargs)
