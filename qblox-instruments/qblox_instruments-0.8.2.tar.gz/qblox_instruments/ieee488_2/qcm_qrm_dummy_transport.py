# ----------------------------------------------------------------------------
# Description    : Transport layer (abstract, IP, file, dummy)
# Git repository : https://gitlab.com/qblox/packages/software/qblox_instruments.git
# Copyright (C) Qblox BV (2020)
# ----------------------------------------------------------------------------


# -- include -----------------------------------------------------------------

import os
import sys
import struct
import subprocess
from copy import deepcopy

from typing import Union, Iterable, Dict
from qblox_instruments import PulsarType, ClusterType
from qblox_instruments.ieee488_2 import (
        DummyTransport,
        DummyBinnedAcquisitionData,
        DummyScopeAcquisitionData,
)


# -- class -------------------------------------------------------------------

class QcmQrmDummyTransport(DummyTransport):
    """
    Class to replace a QCM/QRM module with a dummy device to support software
    stack testing without hardware. The class implements all mandatory,
    required and QCM/QRM specific SCPI calls. Call reponses are largely
    artifically constructed to be inline with the call's functionality (e.g.
    `*IDN?` returns valid, but artificial IDN data.) To assist development,
    the Q1ASM assembler has been completely implemented. Please have a look
    at the call's implentation to know what to expect from its response.
    """

    # ------------------------------------------------------------------------
    def __init__(
        self,
        dummy_type: Union[PulsarType, ClusterType],
        scope_acq_cfg_format: str,
        qcm_seq_cfg_format: str,
        qrm_seq_cfg_format: str,
    ):
        """
        Create QCM/QRM dummy transport class.

        Parameters
        ----------
        dummy_type : Union[PulsarType, ClusterType]
            Dummy module type (e.g. Pulsar QCM, Pulsar QRM)
        scope_acq_cfg_format : str
            Configuration format based on
            `struct.pack <https://docs.python.org/3/library/struct.html>`_
            format used to calculate scope acquisition configuration
            transaction size.
        qcm_seq_cfg_format : str
            QCM sequencer configuration format based on
            `struct.pack <https://docs.python.org/3/library/struct.html>`_
            format used to calculate scope acquisition configuration
            transaction size.
        qrm_seq_cfg_format : str
            QRM sequencer configuration format based on
            `struct.pack <https://docs.python.org/3/library/struct.html>`_
            format used to calculate scope acquisition configuration
            transaction size.

        Returns
        ----------

        Raises
        ----------
        """

        # Initialize base class
        super().__init__(dummy_type)

        # Initialize variables
        self._asm_status = False
        self._asm_log = ""
        self._acq_scope_cfg = {}
        self._sequencer_cfg = {}
        self._acq_scope_cfg_bin_size = struct.calcsize(scope_acq_cfg_format)
        if self.is_qcm_type:
            self._sequencer_cfg_bin_size = struct.calcsize(qcm_seq_cfg_format)
        else:
            self._sequencer_cfg_bin_size = struct.calcsize(qrm_seq_cfg_format)
        self._awg_waveforms = {}
        self._acq_weights = {}
        self._acq_acquisitions = {}
        self._acq_scope_acquisition = None
        self._channelmap = {}
        self._port_cfg = {}

        # Set command dictionary
        self._cmds["LO:PRESent?"] = self._get_lo_hw_present
        self._cmds["STATus:ASSEMbler:SUCCess?"] = self._get_assembler_status
        self._cmds["STATus:ASSEMbler:LOG?"] = self._get_assembler_log
        self._cmds["ACQ:SCOpe:CONFiguration"] = self._set_acq_scope_config
        self._cmds["ACQ:SCOpe:CONFiguration?"] = self._get_acq_scope_config
        self._cmds["SEQuencer#:PROGram"] = self._set_sequencer_program
        self._cmds["SEQuencer#:CONFiguration"] = self._set_sequencer_config
        self._cmds["SEQuencer#:CONFiguration?"] = self._get_sequencer_config
        self._cmds["SEQuencer#:STATE?"] = self._get_sequencer_state
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:NEW"] = self._add_awg_waveform
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:DELete"] = self._del_awg_waveform
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:DATA"] = self._set_awg_waveform_data
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:DATA?"] = self._get_awg_waveform_data
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:INDex"] = self._set_awg_waveform_index
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:INDex?"] = self._get_awg_waveform_index
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:LENGth?"] = self._get_awg_waveform_length
        self._cmds["SEQuencer#:AWG:WLISt:WAVeform:NAME?"] = self._get_awg_waveform_name
        self._cmds["SEQuencer#:AWG:WLISt:SIZE?"] = self._get_num_awg_waveforms
        self._cmds["SEQuencer#:AWG:WLISt?"] = self._get_awg_waveforms
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:NEW"] = self._add_acq_weight
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:DELete"] = self._del_acq_weight
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:DATA"] = self._set_acq_weight_data
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:DATA?"] = self._get_acq_weight_data
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:INDex"] = self._set_acq_weight_index
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:INDex?"] = self._get_acq_weight_index
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:LENGth?"] = self._get_acq_weight_length
        self._cmds["SEQuencer#:ACQ:WLISt:WEIght:NAME?"] = self._get_acq_weight_name
        self._cmds["SEQuencer#:ACQ:WLISt:SIZE?"] = self._get_num_acq_weights
        self._cmds["SEQuencer#:ACQ:WLISt?"] = self._get_acq_weights
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:NEW"] = self._add_acq_acquisition
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:DELete"] = self._del_acq_acquisition
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:DATA"] = self._set_acq_acquisition_data
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:DATA?"] = self._get_acq_acquisition_data
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:INDex"] = self._set_acq_acquisition_index
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:INDex?"] = self._get_acq_acquisition_index
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:NUM_BINS?"] = self._get_acq_acquisition_num_bins
        self._cmds["SEQuencer#:ACQ:ALISt:ACQuisition:NAME?"] = self._get_acq_acquisition_name
        self._cmds["SEQuencer#:ACQ:ALISt:SIZE?"] = self._get_num_acq_acquisitions
        self._cmds["SEQuencer#:ACQ:ALISt?"] = self._get_acq_acquisitions
        self._cmds["SEQuencer#:CHANnelmap"] = self._set_channelmap
        self._cmds["SEQuencer#:CHANnelmap?"] = self._get_channelmap
        self._cmds["AFE:ATT:OUT#"] = self._set_out_att
        self._cmds["AFE:ATT:OUT#?"] = self._get_out_att
        self._cmds["AFE:ATT:IN#"] = self._set_in_att
        self._cmds["AFE:ATT:IN#?"] = self._get_in_att

    # ------------------------------------------------------------------------
    @property
    def is_qcm_type(self) -> bool:
        """
        Return if module is of type QCM.

        Parameters
        ----------

        Returns
        ----------
        bool
            True if module is of type QCM.

        Raises
        ----------
        """

        return self._type_handle.is_qcm_type

    # ------------------------------------------------------------------------
    @property
    def is_qrm_type(self) -> bool:
        """
        Return if module is of type QRM.

        Parameters
        ----------

        Returns
        ----------
        bool
            True if module is of type QRM.

        Raises
        ----------
        """

        return self._type_handle.is_qrm_type

    # ------------------------------------------------------------------------
    @property
    def is_rf_type(self) -> bool:
        """
        Return if module is of type QCM-RF or QRM-RF.

        Parameters
        ----------

        Returns
        ----------
        bool
            True if module is of type QCM-RF or QRM-RF.

        Raises
        ----------
        """

        return self._type_handle.is_rf_type

    # ------------------------------------------------------------------------
    def set_dummy_binned_acquisition_data(
            self,
            sequencer: int,
            acq_index_name: str,
            data: Iterable[Union[DummyBinnedAcquisitionData, None]]):
        """
        Set dummy binned acquisition data for the dummy.

        Parameters
        ----------
        sequencer : int
            Sequencer.
        acq_index_name : str
            Acquisition index name.
        data : Iterable[Union[DummyBinnedAcquisitionData, None]]
            Dummy data for the binned acquisition.
            An iterable of all the bin values.

        Returns
        ----------

        Raises
        ----------
        """

        def _unnormalized_int(single_data: DummyBinnedAcquisitionData):
            sample_width = 12
            max_sample_value = 2 ** (sample_width - 1) - 1
            max_sample_value_sqrd = max_sample_value ** 2

            int0, int1 = single_data.data[0], single_data.data[1]
            int0 *= max_sample_value_sqrd * (single_data.avg_cnt or 1)
            int1 *= max_sample_value_sqrd * (single_data.avg_cnt or 1)
            return [round(int0), round(int1)]

        sequencer = str(sequencer)
        if sequencer not in self._acq_acquisitions:
            self._acq_acquisitions[sequencer] = {}

        bins = []
        for single_data in data:
            if single_data is None:
                bins.append({
                    "valid": False,
                    "int": [0, 0],
                    "thres": 0,
                    "avg_cnt": 0})
            else:
                bins.append({
                    "valid": True,
                    "int": _unnormalized_int(single_data),
                    "thres": round(single_data.thres * (single_data.avg_cnt or 1)),
                    "avg_cnt": single_data.avg_cnt})

        if acq_index_name not in self._acq_acquisitions[sequencer]:
            self._acq_acquisitions[sequencer][acq_index_name] = {}
        if "acq" not in self._acq_acquisitions[sequencer][acq_index_name]:
            self._acq_acquisitions[sequencer][acq_index_name]["acq"] = {}
        self._acq_acquisitions[sequencer][acq_index_name]["acq"]["bins"] = bins

    # ------------------------------------------------------------------------
    def set_dummy_scope_acquisition_data(
            self,
            data: DummyScopeAcquisitionData):
        """
        Set dummy scope acquisition data for the dummy.

        Parameters
        ----------
        data : DummyScopeAcquisitionData
             Dummy data for the scope acquisition.

        Returns
        ----------

        Raises
        ----------
        """

        def _unnormalized_int(val, avg_cnt):
            sample_width = 12
            max_sample_value = 2 ** (sample_width - 1) - 1
            return round(val * max_sample_value * (avg_cnt or 1))

        def _pack_data(data):
            return struct.pack("i" * len(data), *data)

        converted_data = ([], [])
        for single_data in data.data:
            converted_data[0].append(_unnormalized_int(single_data[0], data.avg_cnt[0]))
            converted_data[1].append(_unnormalized_int(single_data[1], data.avg_cnt[1]))

        self._acq_scope_acquisition = {
            "data": (_pack_data(converted_data[0]), _pack_data(converted_data[1])),
            "or": data.out_of_range,
            "avg_cnt": data.avg_cnt,
        }

    # ------------------------------------------------------------------------
    def _get_lo_hw_present(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler status. Refer to the assembler log to get more
        information regarding the assembler result.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = str(int(self.is_rf_type))

    # ------------------------------------------------------------------------
    def _get_assembler_status(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler status. Refer to the assembler log to get more
        information regarding the assembler result.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = str(int(self._asm_status))

    # ------------------------------------------------------------------------
    def _get_assembler_log(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get assembler log.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._bin_out = self._encode_bin(self._asm_log.encode())

    # ------------------------------------------------------------------------
    def _set_acq_scope_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of scope acquisition; untouched and in binary
        format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._acq_scope_cfg = self._decode_bin(bin_in)

    # ------------------------------------------------------------------------
    def _get_acq_scope_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of scope acquisition. If no
        configuration was previously stored an array of zero bytes is
        returned. The length of the returned array is calculated based on the
        configuration format set during initialization of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if len(self._acq_scope_cfg) > 0:
            self._bin_out = self._encode_bin(self._acq_scope_cfg)
        else:
            self._bin_out = self._encode_bin(self._acq_scope_cfg_bin_size * b"\x00")

    # ------------------------------------------------------------------------
    def _set_sequencer_program(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Runs provided sequencer Q1ASM program through assembler. The assembler
        is a pre-compiled application, which is selected based on the platform
        this method is called on. The assembler status and log are stored and
        can be retrieved using corresponding methods. On a failure to assemble
        an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        q1asm_str = self._decode_bin(bin_in).decode()
        fid = open("./tmp.q1asm", "w")
        fid.write(q1asm_str)
        fid.close()

        if os.name == "nt":  # Windows
            assembler_path = os.path.abspath(
                os.path.dirname(os.path.abspath(__file__))
                + "../../assemblers/q1asm_windows.exe"
            )
            proc = subprocess.Popen(
                [assembler_path, "-o", "tmp", "tmp.q1asm"],
                shell=True,
                text=True,
                bufsize=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        elif sys.platform == "darwin":  # MacOS
            assembler_path = os.path.abspath(
                os.path.dirname(os.path.abspath(__file__))
                + "../../assemblers/q1asm_macos"
            )
            proc = subprocess.Popen(
                [assembler_path + " -o tmp tmp.q1asm"],
                shell=True,
                text=True,
                bufsize=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        else:  # Linux
            assembler_path = os.path.abspath(
                os.path.dirname(os.path.abspath(__file__))
                + "../../assemblers/q1asm_linux"
            )
            proc = subprocess.Popen(
                [assembler_path + " -o tmp tmp.q1asm"],
                shell=True,
                text=True,
                bufsize=1,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        self._asm_log = proc.communicate()[0]
        self._asm_status = not proc.returncode

        if not self._asm_status:
            self._system_error.append("Assembly failed.")

    # ------------------------------------------------------------------------
    def _set_sequencer_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Stores configuration of indexed sequencer; untouched and in binary
        format.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._sequencer_cfg[cmd_params[0]] = self._decode_bin(bin_in)

    # ------------------------------------------------------------------------
    def _get_sequencer_config(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Retrieves previously stored configuration of the indexed sequencer.
        If no configuration was previously stored an array of zero bytes is
        returned. The length of the returned array is calculated based on the
        configuration format set during initialization of the class.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._sequencer_cfg:
            self._bin_out = self._encode_bin(self._sequencer_cfg[cmd_params[0]])
        else:
            self._bin_out = self._encode_bin(self._sequencer_cfg_bin_size * b"\x00")

    # ------------------------------------------------------------------------
    def _get_sequencer_state(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get sequencer state.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = "STOPPED;FORCED STOP,ACQ BINNING DONE,"

    # ------------------------------------------------------------------------
    def _add_awg_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds waveform to the waveform list of the indexed sequencer's AWG
        path. If the waveform name is already in use, an error is set in
        system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                error = "Waveform {} already in waveform list.".format(cmd_args[0])
                self._system_error.append(error)
                return

            for index in range(0, len(self._awg_waveforms[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._awg_waveforms[cmd_params[0]]:
                    if self._awg_waveforms[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused is True:
                    break
        else:
            self._awg_waveforms[cmd_params[0]] = {}
            index = 0

        self._awg_waveforms[cmd_params[0]][cmd_args[0]] = {
            "wave": bytearray([]),
            "index": index,
        }

    # ------------------------------------------------------------------------
    def _del_awg_waveform(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes waveform from the waveform list of the indexed sequencer's
        AWG path. If the waveform name does not exist, an error is set in
        system error. The names "all" and "ALL" are reserved and those are
        deleted all waveforms in the waveform list of the indexed sequencer's
        AWG path are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_args[0].lower() == "all":
            self._awg_waveforms[cmd_params[0]] = {}
        else:
            if cmd_params[0] in self._awg_waveforms:
                if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                    del self._awg_waveforms[cmd_params[0]][cmd_args[0]]
                    return
            error = "Waveform {} does not exist in waveform list.".format(cmd_args[0])
            self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_awg_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform data for the waveform in the waveform list of the
        indexed sequencer's AWG path. If the waveform name does not exist,
        an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"] = self._decode_bin(bin_in)
                return
        error = "Waveform {} does not exist in waveform list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_awg_waveform_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform data of the waveform in the waveform list of the indexed
        sequencer's AWG path. If the waveform name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._bin_out = self._encode_bin(
                    self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"]
                )
                return
        error = "Waveform {} does not exist in waveform list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_awg_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets waveform index of the waveform in the waveform list of the
        indexed sequencer's AWG path. If the waveform name does not exist or
        the index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                for name in self._awg_waveforms[cmd_params[0]]:
                    if (self._awg_waveforms[cmd_params[0]][name]["index"] == cmd_args[1] and
                       name != cmd_args[0]):
                        error = "Waveform index {} already in use by {}.".format(cmd_args[0], name)
                        self._system_error.append(error)
                        return
                self._awg_waveforms[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
                return
        error = "Waveform {} does not exist in waveform list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_awg_waveform_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform index of the waveform in the waveform list of the indexed
        sequencer's AWG path. If the waveform name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._data_out = self._awg_waveforms[cmd_params[0]][cmd_args[0]]["index"]
                return
        error = "Waveform {} does not exist in waveform list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_awg_waveform_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform length of the waveform in the waveform list of the
        indexed sequencer's AWG path. The waveform lenght is returned as the
        number of samples. If the waveform name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if cmd_args[0] in self._awg_waveforms[cmd_params[0]]:
                self._data_out = int(len(self._awg_waveforms[cmd_params[0]][cmd_args[0]]["wave"]) / 4)
                return
        error = "Waveform {} does not exist in waveform list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_awg_waveform_name(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets waveform name of the waveform in the waveform list of the indexed
        sequencer's AWG path. If the waveform name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            for name in self._awg_waveforms[cmd_params[0]]:
                if self._awg_waveforms[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name
                    return
        error = "Waveform {} does not exist in waveform list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_num_awg_waveforms(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Number of waveforms in the waveform list of the indexed sequencer's
        AWG path.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            self._data_out = len(self._awg_waveforms[cmd_params[0]])
        else:
            self._data_out = 0

    # ------------------------------------------------------------------------
    def _get_awg_waveforms(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get every waveform in the waveform list of the indexed sequencer's
        AWG path.The waveforms are returned in a binary structure.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._awg_waveforms:
            if len(self._awg_waveforms[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True

            self._bin_out = self._encode_bin(
                struct.pack("I", len(self._awg_waveforms[cmd_params[0]])),
                end_of_line
            )

            for it, name in enumerate(self._awg_waveforms[cmd_params[0]]):
                if it < len(self._awg_waveforms[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(
                    name.encode(),
                    False
                )
                self._bin_out += self._encode_bin(
                    struct.pack("I", int(self._awg_waveforms[cmd_params[0]][name]["index"])),
                    False,
                )
                self._bin_out += self._encode_bin(
                    self._awg_waveforms[cmd_params[0]][name]["wave"],
                    end_of_line
                )
        else:
            self._bin_out = self._encode_bin(struct.pack("I", 0), True)

    # ------------------------------------------------------------------------
    def _add_acq_weight(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds weight to the weight list of the indexed sequencer's acquisition
        path. If the weight name is already in use, an error is set in system
        error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                error = "Weight {} already in weight list.".format(cmd_args[0])
                self._system_error.append(error)
                return

            for index in range(0, len(self._acq_weights[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._acq_weights[cmd_params[0]]:
                    if self._acq_weights[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused is True:
                    break
        else:
            self._acq_weights[cmd_params[0]] = {}
            index = 0

        self._acq_weights[cmd_params[0]][cmd_args[0]] = {
            "wave": bytearray([]),
            "index": index,
        }

    # ------------------------------------------------------------------------
    def _del_acq_weight(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes weight from the weight list of the indexed sequencer's
        acquisition path. If the weight name does not exist, an error is set
        in system error. The names "all" and "ALL" are reserved and those are
        deleted all weights in the weight list of the indexed sequencer's
        acquisition path are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_args[0].lower() == "all":
            self._acq_weights[cmd_params[0]] = {}
        else:
            if cmd_params[0] in self._acq_weights:
                if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                    del self._acq_weights[cmd_params[0]][cmd_args[0]]
                    return
            error = "Weight {} does not exist in weight list.".format(cmd_args[0])
            self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_acq_weight_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets weight data for the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist, an
        error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"] = self._decode_bin(bin_in)
                return
        error = "Weight {} does not exist in weight list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_weight_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight data of the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist, an
        error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._bin_out = self._encode_bin(
                    self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"]
                )
                return
        error = "Weight {} does not exist in weight list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_acq_weight_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets weight index of the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist or the
        index is already in use, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                for name in self._acq_weights[cmd_params[0]]:
                    if (self._acq_weights[cmd_params[0]][name]["index"] == cmd_args[1] and
                       name != cmd_args[0]):
                        error = "Weight index {} already in use by {}.".format(cmd_args[0], name)
                        self._system_error.append(error)
                        return
                self._acq_weights[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
                return
        error = "Weight {} does not exist in weight list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_weight_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight index of the weight in the weight list of the indexed
        sequencer's acquisition path. If the weight name does not exist,
        an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._data_out = self._acq_weights[cmd_params[0]][cmd_args[0]]["index"]
                return
        error = "Weight {} does not exist in weight list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_weight_length(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight length of the weight in the weight list of the indexed
        sequencer's acquisition path. The weight lenght is returned as the
        number of samples. If the weight name does not exist, an error is set
        in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if cmd_args[0] in self._acq_weights[cmd_params[0]]:
                self._data_out = int(len(self._acq_weights[cmd_params[0]][cmd_args[0]]["wave"]) / 4)
                return
        error = "Weight {} does not exist in weight list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_weight_name(
        self, cmd_params: list, cmd_args: list, bin_in: bytes
    ) -> None:
        """
        Gets weight name of the weight in the weight list of the indexed sequencer's acquisition path.
        If the weight name does not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            for name in self._acq_weights[cmd_params[0]]:
                if self._acq_weights[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name
                    return
        error = "Weight {} does not exist in weight list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_num_acq_weights(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets weight name of the weight in the weight list of the indexed
        sequencer's acquistion path. If the weight name does not exist, an
        error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            self._data_out = len(self._acq_weights[cmd_params[0]])
        else:
            self._data_out = 0

    # ------------------------------------------------------------------------
    def _get_acq_weights(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get every weight in the weight list of the indexed sequencer's
        acquistition path. The weights are returned in a binary structure.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_weights:
            if len(self._acq_weights[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True

            self._bin_out = self._encode_bin(
                struct.pack("I", len(self._acq_weights[cmd_params[0]])),
                end_of_line
            )

            for it, name in enumerate(self._acq_weights[cmd_params[0]]):
                if it < len(self._acq_weights[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(
                    name.encode(),
                    False
                )
                self._bin_out += self._encode_bin(
                    struct.pack("I", int(self._acq_weights[cmd_params[0]][name]["index"])),
                    False,
                )
                self._bin_out += self._encode_bin(
                    self._acq_weights[cmd_params[0]][name]["wave"],
                    end_of_line
                )
        else:
            self._bin_out = self._encode_bin(struct.pack("I", 0), True)

    # ------------------------------------------------------------------------
    def _add_acq_acquisition(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Add acquisition to acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                error = "Acquisition {} already in acquisition list.".format(cmd_args[0])
                self._system_error.append(error)
                return

            for index in range(0, len(self._acq_acquisitions[cmd_params[0]]) + 1):
                idx_unused = True
                for name in self._acq_acquisitions[cmd_params[0]]:
                    if self._acq_acquisitions[cmd_params[0]][name]["index"] == index:
                        idx_unused = False
                        break
                if idx_unused is True:
                    break
        else:
            self._acq_acquisitions[cmd_params[0]] = {}
            index = 0

        if cmd_args[0] not in self._acq_acquisitions[cmd_params[0]]:
            self._acq_acquisitions[cmd_params[0]][cmd_args[0]] = {}

        self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["index"] = index

        if "acq" not in self._acq_acquisitions[cmd_params[0]][cmd_args[0]]:
            self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"] = {}
        if "scope" not in self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]:
            self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"] = {
                "data": [bytearray([]), bytearray([])],
                "or": [False, False],
                "avg_cnt": [0, 0],
            }
        if "bins" not in self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]:
            self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"] = [
                {"valid": False, "int": [0, 0], "thres": 0, "avg_cnt": 0}
                for _ in range(int(cmd_args[1]))
            ]

    # ------------------------------------------------------------------------
    def _del_acq_acquisition(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Deletes acquisition from the acquisition list of the indexed
        sequencer. If the acquisition name does not exist, an error is set in
        system error. The names "all" and "ALL" are reserved and those are
        deleted all acquisitions in the acquisition list of the indexed
        sequencer are deleted.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0].lower() == "all":
                self._acq_acquisitions[cmd_params[0]] = {}
            else:
                if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                    del self._acq_acquisitions[cmd_params[0]][cmd_args[0]]
                    return
                error = "Acquisition {} does not exist in acquisition list.".format(cmd_args[0])
                self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Adds scope acquisition data to the selected acquisition in the
        specified sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                if self._acq_scope_acquisition is not None:
                    self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"] = self._acq_scope_acquisition
                return
        error = "Acquisition {} does not exist in acquisition list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_data(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get acquisition data of a single acquisition from the specified
        sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                self._bin_out = self._encode_bin(
                    self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["data"][0],
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack("?", self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["or"][0]),
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack("I", self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["avg_cnt"][0]),
                    False,
                )
                self._bin_out += self._encode_bin(
                    self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["data"][1],
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack("?", self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["or"][1]),
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack("I", self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["scope"]["avg_cnt"][1]),
                    False,
                )

                num_bins = len(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"])
                bins = []
                for bin_it in range(0, num_bins):
                    bins.append(int(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["valid"]))
                    bins.append(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["int"][0])
                    bins.append(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["int"][1])
                    bins.append(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["thres"])
                    bins.append(self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["acq"]["bins"][bin_it]["avg_cnt"])
                self._bin_out += self._encode_bin(
                    struct.pack("=" + num_bins * "QqqLL", *bins),
                    True,
                )
                return
        error = "Acquisition {} does not exist in acquisition list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _set_acq_acquisition_index(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets acquisition index of the acquisition in the acquisition list
        of the indexed sequencer's acquisition path. If the acquisition name
        does not exist or the index is already in use, an error is set in
        system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                for name in self._acq_acquisitions[cmd_params[0]]:
                    if (self._acq_acquisitions[cmd_params[0]][name]["index"] == cmd_args[1] and
                       name != cmd_args[0]):
                        error = "Acquisition index {} already in use by {}.".format(cmd_args[0], name)
                        self._system_error.append(error)
                        return
                self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["index"] = cmd_args[1]
                return
        error = "Acquisition {} does not exist in acquisition list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_index(
        self, cmd_params: list, cmd_args: list, bin_in: bytes
    ) -> None:
        """
        Gets acquisition index of the acquisition in the acquisition list of
        the indexed sequencer's acquisition path. If the acquisition name does
        not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                self._data_out = self._acq_acquisitions[cmd_params[0]][cmd_args[0]]["index"]
                return
        error = "Acquisition {} does not exist in acquisition list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_num_bins(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Get number of bins of the acquisition in the specified sequencer's
        acquisition list. If the acquisition name does not exist, an error is
        set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if cmd_args[0] in self._acq_acquisitions[cmd_params[0]]:
                self._data_out = int(
                    len(self._acq_acquisitions[cmd_params[0]]["acq"]["bins"])
                )
                return
        error = "Acquisition {} does not exist in acquisition list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_acq_acquisition_name(
        self, cmd_params: list, cmd_args: list, bin_in: bytes
    ) -> None:
        """
        Gets acquisition name of the acquisition in the acquisition list of
        the indexed sequencer's acquisition path. If the acquisition name does
        not exist, an error is set in system error.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            for name in self._acq_acquisitions[cmd_params[0]]:
                if self._acq_acquisitions[cmd_params[0]][name]["index"] == cmd_args[0]:
                    self._data_out = name
                    return
        error = "Acquisition {} does not exist in acquisition list.".format(cmd_args[0])
        self._system_error.append(error)

    # ------------------------------------------------------------------------
    def _get_num_acq_acquisitions(
        self, cmd_params: list, cmd_args: list, bin_in: bytes
    ) -> None:
        """
        Get number of acquisitions in the specified sequencer's acquisition
        list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        self._data_out = 0
        if cmd_params[0] in self._acq_acquisitions:
            self._data_out = len(self._acq_acquisitions[cmd_params[0]])
            return

    # ------------------------------------------------------------------------
    def _get_acq_acquisitions(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Return all acquisitions in the specied sequencer's acquisition list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """

        if cmd_params[0] in self._acq_acquisitions:
            if len(self._acq_acquisitions[cmd_params[0]]) > 0:
                end_of_line = False
            else:
                end_of_line = True

            self._bin_out = self._encode_bin(
                struct.pack("I", len(self._acq_acquisitions[cmd_params[0]])),
                end_of_line,
            )

            for it, name in enumerate(self._acq_acquisitions[cmd_params[0]]):
                if it < len(self._acq_acquisitions[cmd_params[0]]) - 1:
                    end_of_line = False
                else:
                    end_of_line = True

                self._bin_out += self._encode_bin(name.encode(), False)
                self._bin_out += self._encode_bin(
                    struct.pack("I", int(self._acq_acquisitions[cmd_params[0]][name]["index"])),
                    False,
                )

                self._bin_out += self._encode_bin(
                    self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["data"][0],
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack("?", self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["or"][0]),
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack("I", self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["avg_cnt"][0]),
                    False,
                )
                self._bin_out += self._encode_bin(
                    self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["data"][1],
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack("?", self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["or"][1]),
                    False,
                )
                self._bin_out += self._encode_bin(
                    struct.pack("I", self._acq_acquisitions[cmd_params[0]][name]["acq"]["scope"]["avg_cnt"][1]),
                    False,
                )

                num_bins = len(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"])
                bins = []
                for bin_it in range(0, num_bins):
                    bins.append(int(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["valid"]))
                    bins.append(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["int"][0])
                    bins.append(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["int"][1])
                    bins.append(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["thres"])
                    bins.append(self._acq_acquisitions[cmd_params[0]][name]["acq"]["bins"][bin_it]["avg_cnt"])
                self._bin_out += self._encode_bin(
                    struct.pack("=" + num_bins * "QqqLL", *bins),
                    end_of_line
                )
        else:
            self._bin_out = self._encode_bin(struct.pack("I", 0), True)

    # ------------------------------------------------------------------------
    def _set_channelmap(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the channelmap list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """
        sequencer_idx = cmd_params[0]
        channel_map_bin = self._decode_bin(bin_in)
        channel_map = list(
            struct.unpack("I" * int(len(channel_map_bin) / 4), channel_map_bin)
        )
        self._channelmap[sequencer_idx] = channel_map

    # ------------------------------------------------------------------------
    def _get_channelmap(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the channelmap list. If not set previously, returns an empty list.

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """
        channel_map = list()
        if cmd_params[0] in self._channelmap:
            channel_map = self._channelmap[cmd_params[0]]
        channel_map_packed = struct.pack("I" * len(channel_map), *channel_map)
        self._bin_out = self._encode_bin(channel_map_packed)
        
    # ------------------------------------------------------------------------
    def _set_out_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the output channel map

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["attenuation"] = cmd_args[0]
        self._port_cfg[key] = port
        
    
    # ------------------------------------------------------------------------
    def _get_out_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the output attenuation. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """
        key = f"out{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("attenuation", 0)
        

    # ------------------------------------------------------------------------
    def _set_in_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Sets the output channel map

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """
        key = f"in{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        port["attenuation"] = cmd_args[0]
        self._port_cfg[key] = port
        
    
    # ------------------------------------------------------------------------
    def _get_in_att(self, cmd_params: list, cmd_args: list, bin_in: bytes) -> None:
        """
        Gets the output attenuation. If not set previously, returns 0

        Parameters
        ----------
        cmd_params : list
            Command parameters indicated by '#' in the command.
        cmd_args : list
            Command arguments.
        bin_in : bytes
            Binary input data.

        Returns
        ----------

        Raises
        ----------
        """
        key = f"in{cmd_params[0]}"
        port = self._port_cfg.get(key, {})
        self._data_out = port.get("attenuation", 0)
        
    
