"""
Module containing all hw related controls (LockControl and QrReader classes).
"""

import time
import datetime
import struct

class LockControl:
    """
    Control various types of lock types. Allow user to unlock it for a specified time.
    :param function fn_open: this function sends primitive OPEN signal to lock (apply voltage)
    :param function fn_close: this function sends primitive CLOSE signal to lock (stop applying voltage)
    :param str lock_type: lock type [SZLDS92 (simple default), MZMMS92 (motoric lock)]
    :param int open_interval: how long should be the lock opened (in seconds)
    :param dict additional_lock_info: additional parameters: for MZMMS92 pass additinal_lock_info["preparation_time"] which is the preparation time for this lock
    """
    def __init__(self, fn_open, fn_close, open_interval, lock_type="SZLDS92", additional_lock_info={}):
        self._on = fn_open
        self._off = fn_close
        self._type = lock_type
        self._open_interval = open_interval

        if self._type == "MZMMS92":
            try:
                assert additional_lock_info["preparation_time"] > 2.9
                self._prep_time = additional_lock_info["preparation_time"]
            except (KeyError, AssertionError, TypeError):
                self._prep_time = 2.9

    def open_pulse(self):
        """ Start a procedure to open the lock. This will then keep the lock unlocked for `open_interval` and then lock it again. """

        if self._type == 'SZLDS92':
            # simple lock type; apply voltage to open
            # LOW -> keep opened for "lockOpenInterval" -> HIGH
            self._on() # LOW
            time.sleep(self._open_interval)
            self._off()

        elif self._type == 'MZMMS92':
            # more complicated type
            # apply voltage to retract lock block; apply again (off+on) to insert back
            # open signalizes open relay, not open lock
            # ON --> (at least 2.9 s time window for lock preparation) --> OFF --> keep open for "lockOpenInterval" (at least 0.05 s)
            # --> ON --> at least 0.5 s --> OFF (finalise locking process) 

            # check bounds on preparation time

            # == init unlock ==
            self._on()
            time.sleep(self._prep_time)

            # the lock is now unlocked, apply voltage to lock ==
            self._off()

            if self._open_interval > 0.05:
                time.sleep(self._open_interval)
            else:
                time.sleep(0.05)

            self._on()
            time.sleep(0.5)
            self._off()

            # == may be locked by closing door ==

class QrReader:
    """ Read QR codes from the reader and issue commands back (LED and buzzer control). """
    def __init__(self, serial_object, green_led_interval=0):
        """
        :param serial_object: (py)serial.Serial object with connection details
        :type serial_object: serial.Serial
        :param float lock_open_interval: attempt to sync green LED 
        """
        self._so = serial_object
        self._green_led_time = green_led_interval

    def read(self):
        try:
            data, valid = self._sread(prefix_bytes=0, return_response=True)
        except TypeError:
            # could not unpack data, valid
            return None

        #1
        prefix = data[:4]
        #2
        if valid and prefix == bytes.fromhex("55aa3000"):
            #2.A
            #2.A.1
            return data[6:]
        else:
            return None


    def _sread(self, callback=None, prefix_bytes=6, return_response=False):

        # HEADER [55aa] (2)
        # CMD [30] (1)
        # SUCCESS [00] (1) (or other values in case of failure
        # DATA LENGTH (?)
        # DATA (?)
        # XOR BYTE (1)

        raw_data = self._so.read(1024)

        #1.2
        if len(raw_data) > 0:
            #1.2.A
            #1.2.A.1
            valid = self._valid_msg(raw_data)
            #1.2.A.2
            if callback:
                #1.2.A.2.A
                callback(raw_data[prefix_bytes:-1], valid)
            #1.2.A.3
            if return_response:
                #1.2.A.3.A
                return (raw_data[prefix_bytes:-1], valid)

    def _ssend(self, hex_cmd):
        """
        :param str hex_cmd: command to the reader in hex string, without last xor byte
        :return int: number of sent bytes
        """
        cmd = bytes.fromhex(hex_cmd)
        no_bytes = self._so.write(cmd + bytes([self._xor(cmd)]))
        return no_bytes

    def green_led(self, check=False):
        """
        Light a green led and beep for minimum of 600 ms. Then (if self._green_led_time > 0.7) let only LED on while lock is open a turn off buzzer.
        :param check: if True: return QR reader response (True/False for OK/not OK)
        :return: only if check=True, then returns True if ok, False otherwise
        """
        time.sleep(.05)  # minimal delay so that reader can beep again (once when reads code then when this send command)
        self._ssend("55aa 04 05 00 0C 01 0C 00 00")  # green beep, 600 ms

        # only green, do not beep
        if self._green_led_time > 0.7:  # 600 ms + 50 ms sleep + reserve
            time.sleep(.05)
            multiple_50ms = (self._green_led_time - 0.6) * 20 - 1
            (_, hex_duration) = hex(int(multiple_50ms)).split("x")
            self._ssend("55aa 04 05 00 04 01 " + hex_duration + " 00 00")  # green, config - 600 ms

        if check:
            resp = self._sread(prefix_bytes=0, callback=None, return_response=True)
            return resp == bytes.fromhex("55aa04000000")


    def red_led(self, check=False):
        """ Light a red led and beep for 600 ms """
        time.sleep(.05)  # minimal delay so that reader can beep again (once when reads code then when this send command)
        self._ssend("55aa 04 05 00 0A 01 0C 00 00")  # red beep, 600 ms
        if check:
            resp = self._sread(prefix_bytes=0, callback=None, return_response=True)
            return resp == bytearray.fromhex("55aa04000000")

    def _valid_msg(self, bytea):
        """ checks validity of msg based on last xor byte (xoring whole msg) """
        return bytea[-1] == self._xor(bytea[:-1])

    def _xor(self, bytea):
        """
        Bitwise XOR
        
        :param bytes bytea: bytes to XOR together
        :return bytes: XOR value in byte format
        """
        xor = 0
        for byte in bytea:
            xor ^= byte
        return xor

