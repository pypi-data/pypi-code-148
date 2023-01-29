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

nscq_nvswitch_drv_version = b"/drv/nvswitch/version"
nscq_nvswitch_device_uuid_path = b"/drv/nvswitch/{device}/uuid"
nscq_nvswitch_device_blacklisted = b"/drv/nvswitch/{device}/blacklisted"
nscq_nvswitch_device_pcie_location = b"/drv/nvswitch/{device}/pcie/location"

nscq_nvswitch_phys_id = b"/{nvswitch}/id/phys_id"
nscq_nvswitch_uuid = b"/{nvswitch}/id/uuid"
nscq_nvswitch_arch = b"/{nvswitch}/id/arch"
nscq_nvswitch_nvlink_id = b"/{nvswitch}/id/nvlink"
nscq_nvswitch_firmware_version = b"/{nvswitch}/version/firmware"
nscq_nvswitch_inforom_version = b"/{nvswitch}/version/inforom"
nscq_nvswitch_pcie_location = b"/{nvswitch}/pcie/location"
nscq_nvswitch_fabric_status = b"/{nvswitch}/status/fabric"
nscq_nvswitch_reset_required = b"/{nvswitch}/status/reset_required"
nscq_nvswitch_temperature_current = b"/{nvswitch}/status/temperature/current"
nscq_nvswitch_temperature_limit_slowdown = b"/{nvswitch}/status/temperature/limit_slowdown"
nscq_nvswitch_temperature_limit_shutdown = b"/{nvswitch}/status/temperature/limit_shutdown"
nscq_nvswitch_temperature_sensors = b"/{nvswitch}/status/temperature/sensors"
nscq_nvswitch_error_fatal = b"/{nvswitch}/status/error/fatal"
nscq_nvswitch_error_nonfatal = b"/{nvswitch}/status/error/nonfatal"
nscq_nvswitch_error_history_nvlink = b"/{nvswitch}/status/error/history/nvlink"
nscq_nvswitch_error_history_sxid = b"/{nvswitch}/status/error/history/sxid"
nscq_nvswitch_error_history_ecc_count = b"/{nvswitch}/status/error/history/ecc/count"
nscq_nvswitch_error_history_ecc_log = b"/{nvswitch}/status/error/history/ecc/entry"
nscq_nvswitch_nvlink_throughput_counters = b"/{nvswitch}/nvlink/throughput_counters"
nscq_nvswitch_nvlink_raw_throughput_counters = b"/{nvswitch}/nvlink/raw_throughput_counters"

nscq_nvswitch_nvlink_ports_num = b"/{nvswitch}/nvlink/ports_num"
nscq_nvswitch_nvlink_ports_mask = b"/{nvswitch}/nvlink/ports_mask"
nscq_nvswitch_nvlink_vcs_num = b"/{nvswitch}/nvlink/vcs_num"
nscq_nvswitch_nvlink_clock_info = b"/{nvswitch}/nvlink/clock_info"
nscq_nvswitch_nvlink_voltage_info = b"/{nvswitch}/nvlink/voltage_info"
nscq_nvswitch_nvlink_current_info = b"/{nvswitch}/nvlink/current_info"


nscq_nvswitch_port_link_version = b"/{nvswitch}/nvlink/{port}/link_version"
nscq_nvswitch_port_sublink_width = b"/{nvswitch}/nvlink/{port}/sublink_width"
nscq_nvswitch_port_link_bandwidth = b"/{nvswitch}/nvlink/{port}/link_bandwidth"
nscq_nvswitch_port_remote_device_type = b"/{nvswitch}/nvlink/{port}/remote_device/type"
nscq_nvswitch_port_remote_device_pcie_location = b"/{nvswitch}/nvlink/{port}/remote_device/pcie/location"
nscq_nvswitch_port_remote_device_link = b"/{nvswitch}/nvlink/{port}/remote_device/id/link"
nscq_nvswitch_port_remote_device_nvlink = b"/{nvswitch}/nvlink/{port}/remote_device/id/nvlink"
nscq_nvswitch_port_remote_device_uuid = b"/{nvswitch}/nvlink/{port}/remote_device/id/uuid"

nscq_nvswitch_port_link_status = b"/{nvswitch}/nvlink/{port}/status/link"
nscq_nvswitch_port_reset_required = b"/{nvswitch}/nvlink/{port}/status/reset_required"
nscq_nvswitch_port_error_fatal = b"/{nvswitch}/nvlink/{port}/status/error/fatal"
nscq_nvswitch_port_error_nonfatal = b"/{nvswitch}/nvlink/{port}/status/error/nonfatal"
nscq_nvswitch_port_error_replay_count = b"/{nvswitch}/nvlink/{port}/status/error/replay_count"
nscq_nvswitch_port_error_recovery_count = b"/{nvswitch}/nvlink/{port}/status/error/recovery_count"
nscq_nvswitch_port_error_flit_err_count = b"/{nvswitch}/nvlink/{port}/status/error/flit_err_count"
nscq_nvswitch_port_error_lane_crc_err_count_aggregate = b"/{nvswitch}/nvlink/{port}/status/error/lane_crc_err_count_aggregate"
nscq_nvswitch_port_error_lane_ecc_err_count_aggregate = b"/{nvswitch}/nvlink/{port}/status/error/lane_ecc_err_count_aggregate"
nscq_nvswitch_port_lane_crc_err_count = b"/{nvswitch}/nvlink/{port}/{lane}/status/error/crc_err_count"
nscq_nvswitch_port_lane_ecc_err_count = b"/{nvswitch}/nvlink/{port}/{lane}/status/error/ecc_err_count"
nscq_nvswitch_port_lane_max_correctable_lane_crc_error_rate_daily = b"/{nvswitch}/nvlink/{port}/{lane}/status/error/max_correctable_lane_crc_error_rate/daily"
nscq_nvswitch_port_lane_max_correctable_lane_crc_error_rate_monthly = b"/{nvswitch}/nvlink/{port}/{lane}/status/error/max_correctable_lane_crc_error_rate/monthly"
nscq_nvswitch_port_vc_latency = b"/{nvswitch}/nvlink/{port}/{vc}/latency"
nscq_nvswitch_nvlink_port_throughput_counters = b"/{nvswitch}/nvlink/{port}/throughput_counters"
nscq_nvswitch_nvlink_port_raw_throughput_counters = b"/{nvswitch}/nvlink/{port}/raw_throughput_counters"
nscq_nvswitch_port_rx_sublink_state = b"/{nvswitch}/nvlink/{port}/status/rx_sublink_state"
nscq_nvswitch_port_tx_sublink_state = b"/{nvswitch}/nvlink/{port}/status/tx_sublink_state"
nscq_nvswitch_cci_raw_cmis_presence = b"/{nvswitch}/cci/raw/cmis_presence"
nscq_nvswitch_cci_raw_cmis_lane_mapping = b"/{nvswitch}/cci/raw/cmis_lane_mapping"
nscq_nvswitch_cci_raw_cmis_read = b"/{nvswitch}/cci/raw/cmis_read"
nscq_nvswitch_cci_osfp_presence = b"/{nvswitch}/cci/{osfp}/presence"
nscq_nvswitch_port_link_data_rate = b"/{nvswitch}/nvlink/{port}/link_data_rate"
nscq_nvswitch_cci_num_osfp = b"/{nvswitch}/cci/num_osfp"
nscq_nvswitch_cci_osfp_lane_mapping = b"/{nvswitch}/cci/{osfp}/lane_mapping"
nscq_nvswitch_cci_osfp_cable_type = b"/{nvswitch}/cci/{osfp}/cable_type"
nscq_nvswitch_cci_osfp_module_media_type = b"/{nvswitch}/cci/{osfp}/module_media_type"
nscq_nvswitch_cci_osfp_vendor_name = b"/{nvswitch}/cci/{osfp}/vendor_name"
nscq_nvswitch_cci_osfp_cable_length = b"/{nvswitch}/cci/{osfp}/cable_length"
nscq_nvswitch_cci_osfp_part_number = b"/{nvswitch}/cci/{osfp}/part_number"
nscq_nvswitch_cci_osfp_revision_number = b"/{nvswitch}/cci/{osfp}/revision_number"
nscq_nvswitch_cci_osfp_serial_number = b"/{nvswitch}/cci/{osfp}/serial_number"
nscq_nvswitch_cci_osfp_lane_monitor = b"/{nvswitch}/cci/{osfp}/lane_monitor"
nscq_nvswitch_cci_osfp_module_monitor = b"/{nvswitch}/cci/{osfp}/module_monitor"
nscq_nvswitch_cci_osfp_module_firmware_version = b"/{nvswitch}/cci/{osfp}/module_firmware_version"
nscq_nvswitch_cci_osfp_signal_integrity = b"/{nvswitch}/cci/{osfp}/signal_integrity"
nscq_nvswitch_cci_osfp_data_path_state = b"/{nvswitch}/cci/{osfp}/data_path_state"
