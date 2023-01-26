"""
Get QR code from reader, verify it and open door if QR code ok. 
Possibility to specify virtualized lock and reader in configuration (["virtualMode"]). Virtual lock will only print information about voltage and virtual QR code reader will completely simulate serial communication - see manual for details.
Send used QR codes to server.
"""

from uun_qrdoorlock.hw import LockControl, QrReader
from uun_iot import on
from uun_iot.modules.Module import Module
from uun_iot.utils import get_iso_timestamp
from uun_iot.modules.Module import ConfigScopeEnum

import json
import nacl, nacl.signing
import validators
import urllib
import base64
from datetime import datetime
import threading
import serial

import logging
logger = logging.getLogger(__name__)

class QrLock(Module):
    id = "qrLock"

    def __init__(self, config, uucmd):
        self._uucmd_get_public_key = uucmd[1]
        super().__init__(config=config, uucmd=uucmd[0])

        self._verify_key = nacl.signing.VerifyKey(
                self._c("publicKey"),
                encoder=nacl.encoding.Base16Encoder
                )

        self._init_reader()
        self._init_lock()

    def _init_reader(self):
        so = serial.Serial(
                port=self._c("qrReaderSerialDev"),
                baudrate=115200,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=1
                )
        self._qrreader = QrReader(so, self._c("lockOpenInterval"))

    def _init_lock(self):
        """ Initialize lock control. """
        if not self._c("virtualMode", module=ConfigScopeEnum.GATEWAY):
            from RPi import GPIO
            self._pin = self._c("relayPin")
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._pin, GPIO.OUT, initial=GPIO.HIGH)
            def on():
                GPIO.output(self._pin, GPIO.LOW)
            def off():
                GPIO.output(self._pin, GPIO.HIGH)
        else:
            def on():
                logger.info("applying voltage to lock")
            def off():
                logger.info("stopped applying voltage to lock")

        additional = {}
        if self._c("lockType") == "MZMMS92":
            additional["preparation_time"] = self._c("lockPreparationInterval")

        self._lock = LockControl(on, off, self._c("lockOpenInterval"), self._c("lockType"), additional)

    @on("start")
    def listen_for_qr(self, evs):
        runev, stopev = evs
        while runev.is_set():
            bin_qr_code = self._qrreader.read()
            if bin_qr_code is not None:
                self.control_access(bin_qr_code.decode('ascii'))

    def control_access(self, qr_code):
        """ Given a QR code (string), test validity and decide whether to grant/deny access. """
        valid, key = self._process_and_validate_qr(qr_code)

        if valid:
            logger.info("correct QR key (%s) scanned - opening door", key)
            # send async
            threading.Thread(
                    target=self._log_used_qr,
                    kwargs={
                        "key": key,
                        "timestamp": get_iso_timestamp(datetime.utcnow())
                    }).start()
            self._open()
            return True
        else:
            logger.warning("Access denied.")
            self._qrreader.red_led()
            return False

    def _process_and_validate_qr(self, qr_code):
        """
        Given a QR code (encoded in ascii), try to extract key, validity and signature. Then validate the signature and date.
        If the code is valid, return a tuple (True, key), else return (False, None).
        """

        def fail(log_msg):
            logger.warning(log_msg)
            return (False, None)

        data = qr_code
        # unpack values
        try: 
            message = signature = None

            if (validators.url(data)):
                query = urllib.parse.parse_qs(data)
                if len(query["qrcodeMessage"]) > 0:
                    (message, signature) = query["qrcodeMessage"][0].split("|")

            if message is None and signature is None:
                (message, signature) = data.split("|")

            (key, from_timestamp, to_timestamp) = message.split('-')
        except ValueError:
            return fail("invalid data format. Correct format for qr data: `key-timestamp_from-timestamp_to|signature` or URL parameter qrcodeMessage containing the same format.")

        # validate signature
        try:
            signature_bytes = base64.b64decode(signature)
            self._verify_key.verify(message.encode('ascii'), signature_bytes)
                
        except nacl.exceptions.BadSignatureError:
            return fail("QR code contains forged or corrupted message!")
        except ValueError:
            return fail("Signature must be a hexadecimal byte string.")

        # validate date
        try:
            valid_from = datetime.fromtimestamp(int(from_timestamp))
            valid_to = datetime.fromtimestamp(int(to_timestamp))
            now = datetime.utcnow()
            assert valid_from <= now <= valid_to

        except TypeError:
            return fail("Timestamp data corrupted/not valid (from %s to %s)" % (from_timestamp, to_timestamp))
        except AssertionError:
            return fail("Key not yet valid/has expired (from %s to %s): %s" % (valid_from, valid_to, key))

        # everything ok
        return (True, key)

    def _open(self):
        self._qrreader.green_led()
        self._lock.open_pulse()

    def _log_used_qr(self, key, timestamp):
        """
        Registers an used qr code.
        :param key: (unique key from qr) if present, add key and timestamp to cache then send
        :param timestamp: (timestamp of entry in seconds) if present, add key and timestamp to cache then send
        :return:
        """
        self._storage.append((key, timestamp))
        self.send_used_qr()

    @on("tick")
    def send_used_qr(self):
        """
        Sends used qr codes to server. If there is no internet, just save to file and wait.
        """
        self._send_storage()

    @on("update")
    def update(self):
        resp = self._uucmd_get_public_key()
        if resp is not None:
            if 200 <= resp.status_code < 300:
                pubkey = json.loads(resp.text)["publicKey"]
                self._verify_key = nacl.signing.VerifyKey(
                        pubkey,
                        encoder=nacl.encoding.Base16Encoder
                        )
                self._config[self.id]["publicKey"] = pubkey

            self._init_reader()
            self._init_lock()

    def __del__(self):
        if not self._c("virtualMode", module=ConfigScopeEnum.GATEWAY):
            from RPi import GPIO
            GPIO.cleanup(self._pin)

