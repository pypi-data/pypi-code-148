import cantools
import can
import time
import os
import sys
import logging
from tabulate import tabulate


class CellEmulator:
    """
    This class contains the functions to control the cell emulator and perform diagnostics
    """
    logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

    def __init__(self, address='CellEmulator1'):
        self.db = cantools.database.load_file(os.path.dirname(os.path.abspath(__file__)) + '/cellemulator.dbc')
        self.ce_address = address
        self.bus = None

    def can_connection(self, interface, channel, bitrate):
        can.rc['interface'] = interface
        can.rc['channel'] = channel
        can.rc['bitrate'] = bitrate
        self.bus = can.interface.Bus()

    def switch_on(self):
        """
        This function switches on the CE by setting voltages and turning on the relays for each cell
        """
        voltages = [0.5, 1, 1.5, 2, 2.5]
        self.set_cell_relay_states(1)
        for voltage in voltages:
            logging.info("Ramping up Voltage with: " + str(voltage) + "V")
            self.set_cell_voltages(voltage)
            time.sleep(0.5)

    def switch_off(self):
        """
        This function switches off the cell emulator by turning off the relay and setting voltages to 0
        """
        self.set_cell_voltages(0)
        logging.info(f"Voltages set to 0V")
        self.set_cell_relay_states(0)
        logging.info(f"Cell relay states set to 0")

    def send_command(self, command, wanted=None):
        """
        This function sends the command to the CE over CAN
        :param command: The intended query with correct fields
        :param wanted: None
        :return: cmd_message
        """
        cmd_message = self.db.get_message_by_name('Command')
        data = cmd_message.encode(command, strict=False)
        message = can.Message(arbitration_id=cmd_message.frame_id, data=data, is_extended_id=False)
        self.bus.send(message)
        resp = self.bus.recv(timeout=0.05)
        cnt = 0
        data = None
        wait_time = 2 + time.time()
        while resp is not None and wait_time > time.time():
            cnt += 1
            try:
                if resp is not None:
                    data = self.db.decode_message(resp.arbitration_id, resp.data)
                    # Check if response is from message
                    if command["CellEmulatorAddress"] == data["CellEmulatorAddress"] and \
                            command["CellAddress"] == data["CellAddress"]:
                        if wanted is None or wanted in data:
                            break
            except:
                pass
            resp = self.bus.recv(timeout=0.005)
        # logging.info("Received " + str(cnt) + " Responses")
        return data

    def set_cell_voltages(self, voltage, freq=0, ampl=0):
        """
        This function sets the cell voltages
        :param voltage: Value in Volts
        :param freq: None
        :param ampl: None
        """
        cmd = {'CellEmulatorAddress': self.ce_address, 'CellAddress': 0x1F, 'Operation': 1, 'DeviceID': 1,
               'DAC': voltage, 'freq': freq, 'ampl': ampl}
        self.send_command(cmd)

    def set_single_cell_voltage(self, cell, voltage, freq=0, ampl=0):
        """
        This function sets the cell voltage of a single cell in the CE
        :param cell: Cell ID of which the Voltage needs to be set
        :param voltage: Value in Volts
        :param freq:None
        :param ampl:None
        """
        self.db.get_message_by_name('Command')
        if cell in range(0, 19):
            cmd = {'CellEmulatorAddress': self.ce_address, 'CellAddress': f"Cell{cell}", 'Operation': 1, 'DeviceID': 1,
                   'DAC': voltage, 'freq': freq, 'ampl': ampl}
            self.send_command(cmd)
        else:
            logging.error("ERROR: Cell ID out of range")

    def get_single_cell_voltage(self, cell):
        """
        This function gets the voltage value of a single cell
        :param cell: Cell ID for which the voltage needs to be checked
        :return: Cell voltage in Volts
        """
        self.db.get_message_by_name('Command')
        if cell in range(0, 19):
            cmd = {'CellEmulatorAddress': self.ce_address, 'CellAddress': f"Cell{cell}", 'Operation': 0, 'DeviceID': 2,
                   'ADCChannel': 2, 'ADCVoltage': 0}
            resp = self.send_command(cmd, wanted="ADCVoltage")
            voltage = (resp["ADCVoltage"] / 8388608 - 1) * 4.5
            # logging.info(f"Measured Voltage for Cell{cell} :" + str(voltage) + "V")
            return round(voltage, 3)
        else:
            logging.error("ERROR: Cell ID out of range")
            return False

    def get_single_cell_current(self, cell):
        """
        This function gets the current value of a single cell
        :param cell: Cell ID for which the voltage needs to be checked
        :return: Cell current in milliAmps range
        """
        self.db.get_message_by_name('Command')
        if cell in range(0, 19):
            cmd = {'CellEmulatorAddress': self.ce_address, 'CellAddress': f"Cell{cell}", 'Operation': 0, 'DeviceID': 2,
                   'ADCChannel': 0, 'ADCCurrent': 0}
            resp = self.send_command(cmd, wanted="ADCCurrent")
            current = (((resp["ADCCurrent"] / 8388608 - 1) * 4.5) - 2.25) / 25 / 0.18 * 1000
            # logging.info(f"Measured Current for Cell{cell} :" + str(current) + "mA")
            return round(current, 3)
        else:
            logging.error("ERROR: Cell ID out of range")
            return False

    def get_single_cell_low_current(self, cell):
        """
        This function gets the low current value of a single cell
        :param cell: Cell ID for which the current needs to be checked
        :return: Low current value of Cell in microAmps range
        """
        if cell in range(0, 19):
            cmd = {'CellEmulatorAddress': self.ce_address, 'CellAddress': f"Cell{cell}", 'Operation': 0, 'DeviceID': 2,
                   'ADCChannel': 1, 'ADCLowCurrent': 0}
            resp = self.send_command(cmd, wanted="ADCLowCurrent")
            current = (((resp["ADCLowCurrent"] / 8388608 - 1) * 4.5) - 2.25) / 25 / 43 * 1000
            # logging.info(f"Measured Current for Cell{cell} :" + str(current) + "mA")
            return round(current, 3)
        else:
            logging.error("ERROR: Cell ID out of range")
            return False

    def set_cell_relay_states(self, relay_state):
        """
        This function sets the relay states of the cells in the CE
        :param relay_state: 0|OFF or 1|ON
        :return: success or failure
        """
        cmd = {'CellEmulatorAddress': self.ce_address, 'CellAddress': 0x1F, 'Operation': 1, 'DeviceID': 4,
               'OutputRelays': relay_state}
        resp = self.send_command(cmd)
        if resp is None:
            raise EnvironmentError("FAIL: Relay state not set")
        else:
            return resp

    def set_cell_relay_state(self, cell, relay_state):
        """
        This function sets the relay state of individual cells in teh CE
        :param cell: Cell ID for which the relay_state needs to be set
        :param relay_state: 0|OFF or 1|ON
        :return: success or failure
        """
        cmd = {'CellEmulatorAddress': self.ce_address, 'CellAddress': f"Cell{cell}", 'Operation': 1, 'DeviceID': 4,
               'OutputRelays': relay_state}
        resp = self.send_command(cmd)
        if resp is None:
            raise EnvironmentError("FAIL: Relay state not set")
        else:
            return resp

    def get_ce_state(self):
        """
        This function queries the voltage and current values for the cells of the CE
        :return: Cell Emulator Voltage and Current states
        """
        # Init Struct
        ce_state = {}
        for cell in range(19):
            try:
                ce_state["Cell" + str(cell)] = {"voltage": self.get_single_cell_voltage(cell),
                                                "current": self.get_single_cell_current(cell)
                                                }
            except:
                logging.error(f": Could not get cell state for Cell {cell}")
        return ce_state

    def print_cell_state(self, cell):
        """
        This function prints the voltage and current values for a cell with ID in a tabular form
        :param cell: Cell ID to receive the cell state
        """
        state = self.get_ce_state()
        voltages = ["Voltages [V]"]
        currents = ["Currents [mA]"]
        headers = ["Value"]
        cell_state = "Cell"+str(cell)
        if cell_state in state:
            voltages.append(state[cell_state]['voltage'])
            currents.append(state[cell_state]['current'])
            headers.append(cell_state)
        # print('\n'+tabulate([voltages, currents], headers=headers)+'\n')
        logging.info('\n'+tabulate([voltages, currents], headers=headers)+'\n')

    def print_state(self):
        """
        This function prints the voltage and current values for each cell with ID in a tabular form
        """
        state = self.get_ce_state()
        voltages = ["Voltages [V]"]
        currents = ["Currents [mA]"]
        headers = ["Value"]
        for cell in state:
            voltages.append(state[cell]['voltage'])
            currents.append(state[cell]['current'])
            headers.append(cell)
        # print('\n'+tabulate([voltages, currents], headers=headers)+'\n')
        logging.info('\n'+tabulate([voltages, currents], headers=headers)+'\n')

    def get_fw_versions(self):
        """
        This function gets the FW version of the CE and the number of cells found
        """
        broadcast_id = 0x201
        logging.info("Using broadcast ID " + hex(broadcast_id))
        # Writing FW Update Request
        msg = can.Message(arbitration_id=broadcast_id, data=[ord('F'), ord('W'), ord('?'), 0, 0, 0, 0, 0],
                          is_extended_id=False)
        self.bus.send(msg)
        # Block until ready
        fw_versions = self.read_until_RDY()
        logging.info(f"Found {len(fw_versions)} Cells")
        for i in fw_versions:
            logging.info("Received RDY! from following ID: " + hex(i) + " with FW version: " + str(fw_versions[i]))

    def read_until_RDY(self):
        """
        This function sends a command over CAN bus seeking the fw versions of each cell of the CE
        :return: FW versions on each cell of the CE
        """
        wait_time = 1 + time.time()
        msg = self.bus.recv(timeout=2)
        fw_versions = {}
        logging.info("Searching for controllers.")
        while wait_time > time.time():
            fw_versions[msg.arbitration_id] = msg.data[0:6].decode("ASCII")
            sys.stdout.write(".")
            sys.stdout.flush()
            msg = self.bus.recv(timeout=1)
        return fw_versions
