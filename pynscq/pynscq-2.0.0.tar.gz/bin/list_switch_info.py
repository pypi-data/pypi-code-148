#!/usr/bin/env python

import argparse
from collections import defaultdict
from ctypes import *
from pynscq import *

offset = '    '
deviceInformation = defaultdict(dict)

@nscqCallback(p_nscq_uuid_t, nscq_rc_t, p_nscq_uuid_t, user_data_type)
def device_uuid_callback(device, rc, uuid, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    deviceInformation[label.data.decode("UTF-8")]["label"] = label.data.decode("UTF-8")
    deviceInformation[label.data.decode("UTF-8")]["uuid"] = nscq_uuid_t.from_buffer_copy(uuid.contents)

@nscqCallback(p_nscq_uuid_t, nscq_rc_t, nscq_nvlink_clock_info_t, ctypes.c_void_p)
def cci_nvlink_clock_info_callback(uuid, rc, clock_info, _user_data):
    if rc.value == nscq_rcs.NSCQ_RC_ERROR_NOT_IMPLEMENTED:
        return

    label = nscq_uuid_to_label(uuid.contents)
    print (label.data.decode("UTF-8"), " freq_khz: ", clock_info.freq_khz)
    print (label.data.decode("UTF-8"), " vcofreq_khz: ", clock_info.vcofreq_khz)

@nscqCallback(p_nscq_uuid_t, nscq_rc_t, nscq_nvlink_voltage_info_t, ctypes.c_void_p)
def cci_nvlink_voltage_info_callback(uuid, rc, voltage_info, _user_data):
    if rc.value == nscq_rcs.NSCQ_RC_ERROR_NOT_IMPLEMENTED:
        return

    label = nscq_uuid_to_label(uuid.contents)
    print (label.data.decode("UTF-8"), " voltage_mvolt: ", voltage_info.voltage_mvolt)

@nscqCallback(p_nscq_uuid_t, nscq_rc_t, nscq_nvlink_current_info_t, ctypes.c_void_p)
def cci_nvlink_current_info_callback(uuid, rc, current_info, _user_data):
    if rc.value == nscq_rcs.NSCQ_RC_ERROR_NOT_IMPLEMENTED:
        return

    label = nscq_uuid_to_label(uuid.contents)
    print (label.data.decode("UTF-8"), " iddq: ", current_info.iddq)
    print (label.data.decode("UTF-8"), " iddq_rev: ", current_info.iddq_rev)
    print (label.data.decode("UTF-8"), " iddq_dvdd: ", current_info.iddq_dvdd)

@nscqCallback(p_nscq_uuid_t, nscq_rc_t, nscq_temperature_sensors_t, ctypes.c_void_p)
def status_temperature_sensors_callback(uuid, rc, temp_sensors, _user_data):
    if rc.value == nscq_rcs.NSCQ_RC_ERROR_NOT_IMPLEMENTED:
        return

    label = nscq_uuid_to_label(uuid.contents)
    for i in range (0, temp_sensors.num_sensor):
        print("sensor[", i, "]: ", temp_sensors.sensors[i])

with NSCQSession() as session:
    #session.path_observe(b"/drv/nvswitch/version", drv_version_callback)
    print("nscq_api_version %s" % nscq_api_version)
    session.path_observe(b"/drv/nvswitch/{device}/uuid", device_uuid_callback)
    for key in deviceInformation:
        session.mount(deviceInformation[key]["uuid"])

    print("test nvlink clock_info")
    session.path_observe(b"/{nvswitch}/nvlink/clock_info", cci_nvlink_clock_info_callback)

    print("test nvlink voltage_info")
    session.path_observe(b"/{nvswitch}/nvlink/voltage_info", cci_nvlink_voltage_info_callback)

    print("test nvlink current_info")
    session.path_observe(b"/{nvswitch}/nvlink/current_info", cci_nvlink_current_info_callback)

    print("test status temperature sensors")
    session.path_observe(b"/{nvswitch}/status/temperature/sensors", status_temperature_sensors_callback)

