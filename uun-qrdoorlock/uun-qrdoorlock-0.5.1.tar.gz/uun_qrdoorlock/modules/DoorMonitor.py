"""
Door Monitor

Monitor door state based on GPIO interrupts. When doors are opened, it sets one GPIO HIGH and this triggers interrupt.
Thus there is no need to run some methods continuously in a loop to acquire state of the door.
Sends notice to server if they are opened for more time than they should be (possible intrusion/cheating).
"""

from uun_iot import on_tick
from uun_iot.utils import get_iso_timestamp
from uun_iot.module.Module import Module

import RPi.GPIO as GPIO
import requests
import json
import time
import datetime
import threading

import logging
logger = logging.getLogger(__name__)

class DoorMonitor(Module):
    id = "doorMonitor"

    def __init__(self, config, uucmd):
        super().__init__(config=config, uucmd=uucmd)
        
        self._pin = self._c("monitorPin")

        GPIO.setmode(GPIO.BCM)

        # default all pins to LOW
        # pull down resistor, prevent "floating" noise, assure HIGH only when truly connected to HIGH
        GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        # instantaneous door state
        # HIGH means door open
        # LOW means door closed
        self.state = GPIO.input(self._pin)

        # keep track of how long each pin was HIGH (reset when -> LOW)
        if self.state:
            self._timer = None
        else:
            self._timer = time.time()
            # start counting even when doors are initially open
            threading.Thread(target=self._counting_callback).start()

        # register interrupts
        GPIO.add_event_detect(self._pin, GPIO.BOTH, self._monitor_callback, bouncetime=self._c("bounceMs"))

    def _monitor_callback(self):
        """ To be called on each interrupt. """

        self.state = GPIO.input(self._pin)
        now = time.time()

        if input:
            # input went HIGH
            self._timer = now
            logger.warning("doors are opened")
            logger.debug("if doors won't close in %f s, report will be sent to server", self._c("signalAfter"))

            # start counting time in background and send warning to server if doors are opened for more time than is allowed
            self._counting_callback()
        else:
            # input went LOW
            if self._timer is None:
                # doors were opened for too long, report already sent
                pass

            period = now - self._timer
            if period > self._c("signalAfter"):
                self._storage.append({
                    "type": "TooLongOpened.END",
                    "from": get_iso_timestamp(datetime.datetime.fromtimestamp(self._timer)),
                    "to": now,
                    "period": period
                })
                logger.info("doors were opened for more time than allowed but now are closed, sending to server")
                self.send()

            # reset timer
            self._timer = None

    def _counting_callback(self):
        """ Count for how long doors were opened. """
        init_time = self._timer

        # while HIGH
        while self.state:
            print(time.time() - init_time)
            if time.time() - init_time > self._c("signalAfter"):
                self._storage.append({
                    "type": "TooLongOpened.START",
                    "from": get_iso_timestamp(datetime.datetime.fromtimestamp(self._timer)),
                })
                logger.info("doors were opened for more time than allowed, sending warning to server")
                self.send()
                break
            time.sleep(.2)

    @on_tick
    def send(self):
        self._send_storage()

    def __del__(self):
        GPIO.cleanup(self._pin)
