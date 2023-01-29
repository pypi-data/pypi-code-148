#!python

import argparse
from collections import defaultdict
from ctypes import *
from pynscq import *

deviceInformation = defaultdict(dict)
@nscqCallback(p_nscq_uuid_t, nscq_rc_t, p_nscq_uuid_t, user_data_type)
def device_uuid_callback(device, rc, uuid, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    deviceInformation[label.data.decode("UTF-8")]["label"] = label.data.decode("UTF-8")
    deviceInformation[label.data.decode("UTF-8")]["uuid"] = nscq_uuid_t.from_buffer_copy(uuid.contents)


@nscqCallback(p_nscq_uuid_t, nscq_rc_t, nscq_pcie_location_t, ctypes.c_void_p)
def device_pcie_location_callback(uuid, rc, location, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    deviceInformation[label.data.decode("UTF-8")]['pcie_location'] = location


@nscqCallback(p_nscq_uuid_t, nscq_rc_t, nscq_fabric_state_t, ctypes.c_void_p)
def device_fabric_state_callback(uuid, rc, fabric_state, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    deviceInformation[label.data.decode("UTF-8")]['fabric_state'] = fabric_state


@nscqCallback(p_nscq_uuid_t, nscq_rc_t, ctypes.c_bool, ctypes.c_void_p)
def device_reset_required_callback(uuid, rc, reset_required, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    deviceInformation[label.data.decode("UTF-8")]['reset_required'] = reset_required


@nscqCallback(p_nscq_uuid_t, nscq_rc_t, nscq_error_t, ctypes.c_void_p)
def device_fatal_errors_callback(uuid, rc, error, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'fatal_errors' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['fatal_errors'] = []
    deviceInformation[label.data.decode("UTF-8")]['fatal_errors'].append(location)


#_NSCQ_DEF_PATH(nscq_nvswitch_port_link_status, "/{nvswitch}/nvlink/{port}/status/link");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, nscq_rc_t, ctypes.c_uint64, ctypes.c_void_p)
def port_link_status_callback(uuid, port, rc, link, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'port_link_status' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['port_link_status'] = []
    deviceInformation[label.data.decode("UTF-8")]['port_link_status'].append([port, link])

#_NSCQ_DEF_PATH(nscq_nvswitch_port_reset_required,"/{nvswitch}/nvlink/{port}/status/reset_required");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, nscq_rc_t, ctypes.c_bool, ctypes.c_void_p)
def port_reset_required_callback(uuid, port, rc, reset_required, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'port_reset_required' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['port_reset_required'] = []
    deviceInformation[label.data.decode("UTF-8")]['port_reset_required'].append([port, reset_required])

#_NSCQ_DEF_PATH(nscq_nvswitch_port_error_fatal, "/{nvswitch}/nvlink/{port}/status/error/fatal");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, nscq_rc_t, nscq_error_t, ctypes.c_void_p)
def port_fatal_errors_callback(uuid, port, rc, fatal_error, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'port_fatal_errors' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['port_fatal_errors'] = []
    deviceInformation[label.data.decode("UTF-8")]['port_fatal_errors'].append([port, fatal_error])

#_NSCQ_DEF_PATH(nscq_nvswitch_port_error_replay_count, "/{nvswitch}/nvlink/{port}/status/error/replay_count");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, nscq_rc_t, ctypes.c_uint64, ctypes.c_void_p)
def port_error_replay_count_callback(uuid, port, rc, replay_count, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'port_error_replay_count' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['port_error_replay_count'] = []
    deviceInformation[label.data.decode("UTF-8")]['port_error_replay_count'].append([port, replay_count])


#_NSCQ_DEF_PATH(nscq_nvswitch_port_error_recovery_count, "/{nvswitch}/nvlink/{port}/status/error/recovery_count");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, nscq_rc_t, ctypes.c_uint64, ctypes.c_void_p)
def port_error_recovery_count_callback(uuid, port, rc, recovery_count, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'port_error_recovery_count' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['port_error_recovery_count'] = []
    deviceInformation[label.data.decode("UTF-8")]['port_error_recovery_count'].append([port, recovery_count])


#_NSCQ_DEF_PATH(nscq_nvswitch_port_error_flit_err_count, "/{nvswitch}/nvlink/{port}/status/error/flit_err_count");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, nscq_rc_t, ctypes.c_uint64, ctypes.c_void_p)
def port_flit_err_count_callback(uuid, port, rc, flit_err_count, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'port_flit_err_count' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['port_flit_err_count'] = []
    deviceInformation[label.data.decode("UTF-8")]['port_flit_err_count'].append([port, flit_err_count])


#_NSCQ_DEF_PATH(nscq_nvswitch_port_error_lane_crc_err_count_aggregate, "/{nvswitch}/nvlink/{port}/status/error/lane_crc_err_count_aggregate");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, nscq_rc_t, ctypes.c_uint64, ctypes.c_void_p)
def port_crc_err_count_aggregate_callback(uuid, port, rc, lane_crc_err_count, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'crc_err_count_aggregate' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['crc_err_count_aggregate'] = []
    deviceInformation[label.data.decode("UTF-8")]['crc_err_count_aggregate'].append([port, lane_crc_err_count])


#_NSCQ_DEF_PATH(nscq_nvswitch_port_error_lane_ecc_err_count_aggregate, "/{nvswitch}/nvlink/{port}/status/error/lane_ecc_err_count_aggregate");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, nscq_rc_t, ctypes.c_uint64, ctypes.c_void_p)
def port_ecc_err_count_aggregate_callback(uuid, port, rc, lane_ecc_err_count, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'ecc_err_count_aggregate' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['ecc_err_count_aggregate'] = []
    deviceInformation[label.data.decode("UTF-8")]['ecc_err_count_aggregate'].append([port, lane_ecc_err_count])


#_NSCQ_DEF_PATH(nscq_nvswitch_port_lane_crc_err_count, "/{nvswitch}/nvlink/{port}/{lane}/status/error/crc_err_count");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, ctypes.c_uint64, nscq_rc_t, ctypes.c_uint64, ctypes.c_void_p)
def port_crc_err_count_callback(uuid, port, lane, rc, crc_err_count, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'crc_err_count' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['crc_err_count'] = []
    deviceInformation[label.data.decode("UTF-8")]['crc_err_count'].append([port, lane, crc_err_count])


#_NSCQ_DEF_PATH(nscq_nvswitch_port_lane_ecc_err_count, "/{nvswitch}/nvlink/{port}/{lane}/status/error/ecc_err_count");
@nscqCallback(p_nscq_uuid_t, ctypes.c_uint64, ctypes.c_uint64, nscq_rc_t, ctypes.c_uint64, ctypes.c_void_p)
def port_ecc_err_count_callback(uuid, port, lane, rc, ecc_err_count, _user_data):
    label = nscq_uuid_to_label(uuid.contents)
    if 'ecc_err_count' not in deviceInformation[label.data.decode("UTF-8")]:
        deviceInformation[label.data.decode("UTF-8")]['ecc_err_count'] = []
    deviceInformation[label.data.decode("UTF-8")]['ecc_err_count'].append([port, lane, ecc_err_count])


@nscqCallback(nscq_rc_t, ctypes.c_uint32, user_data_type)
def drv_version_callback(rc, version, _user_data):
    global nscq_version
    nscq_version = version


with NSCQSession() as session:
    #session.path_observe(b"/drv/nvswitch/version", drv_version_callback)
    print(nscq_api_version)
    session.path_observe(b"/drv/nvswitch/{device}/uuid", device_uuid_callback)
    for key in deviceInformation:
        session.mount(deviceInformation[key]["uuid"])

    session.path_observe(b"/{nvswitch}/pcie/location", device_pcie_location_callback)
    session.path_observe(b"/{nvswitch}/status/fabric", device_fabric_state_callback)
    session.path_observe(b"/{nvswitch}/status/reset_required", device_reset_required_callback)
    session.path_observe(b"/{nvswitch}/status/error/fatal", device_fatal_errors_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/status/link", port_link_status_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/status/reset_required", port_reset_required_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/status/error/fatal", port_fatal_errors_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/status/error/replay_count", port_error_replay_count_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/status/error/recovery_count", port_error_recovery_count_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/status/error/flit_err_count", port_flit_err_count_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/status/error/lane_crc_err_count_aggregate", port_crc_err_count_aggregate_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/status/error/lane_ecc_err_count_aggregate", port_ecc_err_count_aggregate_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/{lane}/status/error/crc_err_count", port_crc_err_count_callback)
    session.path_observe(b"/{nvswitch}/nvlink/{port}/{lane}/status/error/ecc_err_count", port_ecc_err_count_callback)

parser = argparse.ArgumentParser()

offset = '    '

def pcie_to_string(pcie):
    return "%d:%d:%d:%d"%(pcie.domain, pcie.bus, pcie.device, pcie.function)

def print_port_lane_matrix(data):
    ioffset = '    '
    max_port = data[-1][0]
    max_lane = data[-1][1]
    matrix = [[0 for x in range(max_lane + 1)] for y in range(max_port + 1)]
    for entry in data:
        matrix[entry[0]][entry[1]] = entry[2]
    print(offset+ioffset+"    port:"+"".join('{:4}'.format(i) for i in range(max_port + 1)))
    for lane in range(max_lane + 1):
        output = ""
        for port in range(max_port + 1):
            output += "{:4}".format(matrix[port][lane])
        print(offset+ioffset+ "lane{:4}:".format(lane) + output)

def print_port_info(name, values):
    print(offset+name+":")
    values.sort()
    for value in values:
        print(offset*2+"port: {:4} :: {}".format(value[0], value[1]))


def printer():
    parser = argparse.ArgumentParser()

    card = parser.add_argument_group('card')
    card.add_argument("--pcie", action='store_true')
    card.add_argument("--reset-required", "-rr", action='store_true')
    card.add_argument("--fabric-state", "-fs", action='store_true')
    card.add_argument("--fatal-errors", "-fe", action='store_true')

    port = parser.add_argument_group("port")
    port.add_argument("--port-link-status", "-pls", action='store_true')
    port.add_argument("--port-reset-required", "-prr", action='store_true')
    port.add_argument("--port-fatal-errors", "-pff", action='store_true')
    port.add_argument("--port-replay-count", "-prp", action='store_true')
    port.add_argument("--port-recovery-count","-prc", action='store_true')
    port.add_argument("--flit-err-count", '-flit', action='store_true')
    port.add_argument("--aggregate-crc-err-count", '-acrc', action='store_true')
    port.add_argument("--aggregate-ecc-err-count", '-aecc', action='store_true')

    lane = parser.add_argument_group("port/lane")
    lane.add_argument("--crc-err-count", '-crc', action='store_true')
    lane.add_argument("--ecc-err-count", '-ecc', action='store_true')

    args = parser.parse_args(None)
    printAll = not any(args.__dict__.values())

    print("Major: %d, Minor %d, Patch %d" % (nscq_api_version[0],
                                             nscq_api_version[1],
                                             nscq_api_version[2]))

    for device in deviceInformation:
        print(device)
        devInfo = deviceInformation[device]
        if printAll or args.pcie:
            print(offset+"pcie location: "+pcie_to_string(devInfo['pcie_location']))
        if printAll or args.reset_required:
            print(offset+'reset required: ' + str(devInfo.get('reset_required', None)))
        if printAll or args.fabric_state:
            print(offset+'fabric state: ' + str(devInfo.get('fabric_state', None)))
        if printAll or args.fatal_errors:
            print(offset+'fatal errors: ' + str(devInfo.get('fatal_errors', None)))

        if printAll or args.port_link_status:
            print_port_info('port link status', devInfo.get('port_link_status', []))
        if printAll or args.port_reset_required:
            print_port_info('port reset required', devInfo.get('port_reset_required', []))
        if printAll or args.port_fatal_errors:
            print_port_info('port fatal errors', devInfo.get('port_fatal_errors', []))
        if printAll or args.port_replay_count:
            print_port_info("port replay errors", devInfo.get('port_error_replay_count', []))
        if printAll or args.port_recovery_count:
            print_port_info("port recovery count", devInfo.get('port_error_recovery_count', []))
        if printAll or args.flit_err_count:
            print_port_info('flit err count', devInfo.get('port_flit_err_count', []))
        if printAll or args.aggregate_crc_err_count:
            print_port_info('aggregate crc errors', devInfo.get('crc_err_count_aggregate', []))
        if printAll or args.aggregate_ecc_err_count:
            print_port_info('aggregate ecc errors', devInfo.get('ecc_err_count_aggregate', []))

        if printAll or args.crc_err_count:
            crc_err_count = devInfo.get('crc_err_count', [[]])
            crc_err_count.sort()
            print(offset+"crc err count:")
            print_port_lane_matrix(crc_err_count)
        if printAll or args.ecc_err_count:
            ecc_err_count = devInfo.get('ecc_err_count', [[]])
            ecc_err_count.sort()
            print(offset+"ecc err count:")
            print_port_lane_matrix(ecc_err_count)

if __name__ == "__main__":
    printer()
