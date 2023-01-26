import smbus2 as smbus

import threading
import time
import math
import logging
from typing import List

from uun_iot_libledstrip import rgb2hex
from .LedDev import LedDev
logger = logging.getLogger(__name__)

class I2CPixelDev(LedDev):
    """ 
    Create a pin-based light strip. Each pin controls exactly one light pixel.
    """

    _state: List[tuple]
    _n: int
    _colored: bool
    _lock: threading.Lock

    def __init__(self, pins: List[int], n=None, addr=0x20):
        """
        addr: I2C address of underlying device
        """

        self._max_n = 16
        self._group_size = 0x08

        if n is None:
            n = len(pins)

        if(n > self._max_n):
            raise ValueError(f"This device supports maximum of {self._max_n} pixels.")
        for pin in pins:
            if pin > self._max_n-1:
                raise ValueError(f"This device supports maximum pixel number {self._max_n}, being numbered from 0.")

        if n != len(pins):
            raise ValueError(f"{n=} is not equal to length of pins") 

        self._n = n

        logger.info(f"Initialized a I2CPixelDevice on pins `{pins}` with {self._n} pixels.")
        self._pins = pins
        self._state = [(0,0,0)] * self._n
        self._lock = threading.Lock()

        try:
            self._hw = mcp23016(addr=addr)
        except ChipError:
            self._hw = None
            raise

    def __repr__(self):
        return str([rgb2hex(x) for x in self._state])

    def show(self):
        with self._lock:

            # set 8 bits at a time -- results in two i2c calls
            no_groups = math.ceil(self._n / self._group_size)
            for group_id in range(no_groups):
                mask = 0
                for i in range(self._group_size):
                    k = i + self._group_size*group_id
                    if k >= self._n:
                        break
                    if self._state[k] != (0,0,0):
                        pin = self._pins[k]
                        mask |= (1<<pin)

                self._hw.setGP(group_id, mask)

            # set bits one at a time -- results in 16 i2c calls
            #for i in range(self._n):
            #    pin = self._pins[i]

            #    group = pin // self._group_size
            #    pin_g = pin % self._group_size

            #    if self._state[i] == (0,0,0):
            #        self._hw.pinOff(group, pin_g)
            #    else:
            #        self._hw.pinOn(group, pin_g)

    def __setitem__(self, index, val): 
        with self._lock:
            self._state[index] = val

    def __getitem__(self, index): 
        with self._lock:
            return self._state[index]

    def __del__(self):
        #self._state = [(0,0,0)] * self._n
        if self._hw is None:
            return

        self._hw.pinAllOff()
        self._hw.close()
        #self.show()

class ChipError(Exception):
    pass

class mcp23016():

    def __init__(self, addr = 0x20, active='HIGH', block1_direction = 0x00, block2_direction = 0x00):
        """
        addr: I2C address of MCP23016 device
        active: default state for HIGH state
        block1,2_direction: 1byte, each bit controlls one pin; bit 0 -- output, bit 1 -- input
        """
        self.ADDR = addr
        self.active = (True if active == 'HIGH' else False)

        # block1: 0-7 GPIO, block2: 8-15 GPIO
        # read: get input value
        # write: set output value
        self.GP0   = 0x00  
        self.GP1   = 0x01
        self.OLAT0 = 0x02
        self.OLAT1 = 0x03
        # inverts corresponding inputs
        self.IPOL0 = 0x04
        self.IPOL1 = 0x05
        # bit 0 - output, bit 1 - input
        self.IODIR0 = 0x06
        self.IODIR1 = 0x07
        # interrupts
        self.INTCAP0 = 0x08
        self.INTCAP1 = 0x09

        self.bus=smbus.SMBus(1)

        # last set/got values
        self.olat0 = 0
        self.olat1 = 0
        self.ipol0 = 0
        self.ipol1 = 0
        self.gp0 = 0
        self.gp1 = 0

        # wait before the bus "settles" before writing, otherwise will throw OSError: Remote I/O error.
        time.sleep(1)

        try:
            logger.debug(f"Setting output registers to `{block1_direction:b} {block2_direction:b}`")
            self.bus.write_byte_data(self.ADDR,self.IODIR0,block1_direction)
            self.bus.write_byte_data(self.ADDR,self.IODIR1,block2_direction)
            self.chipOK = True
        except Exception as e:
            self.chipOK = False
            logger.exception(e)

        if not self.chipOK:
            raise ChipError()
        else:
            logger.debug("Directions set ok.")

    def pinOn(self, group, pin):
        """ 
        group: int: 0 or 1
        pin: int: 0-7
        """
        if group == 1:
            if self.active:
                self.olat1 = self.olat1 | (1 << pin)
            else:
                self.olat1 = self.olat1 & (0xff - (1 << pin))
            self.bus.write_byte_data(self.ADDR, self.OLAT1, self.olat1)
        else:
            if self.active:
                self.olat0 = self.olat0 | (1 << pin)
            else:
                self.olat0 = self.olat0 & (0xff - (1 << pin))
            self.bus.write_byte_data(self.ADDR, self.OLAT0, self.olat0)

    def pinOff(self, group, pin):
        """ 
        group: int: 0 or 1
        pin: int: 0-7
        """
        if group == 1:
            if self.active:
                self.olat1 = self.olat1 & (0xff - (1 << pin))
            else:
                self.olat1 = self.olat1 | (1 << pin)
            self.bus.write_byte_data(self.ADDR, self.OLAT1, self.olat1)
        else:
            if self.active:
                self.olat0 = self.olat0 & (0xff - (1 << pin))
            else:
                self.olat0 = self.olat0 | (1 << pin)
            self.bus.write_byte_data(self.ADDR, self.OLAT0, self.olat0)

    def pinAllOff(self):
        #    print ("All off called")
        if self.active:
            self.olat0 = 0x00
        else:
            self.olat0 = 0xFF
        self.bus.write_byte_data(self.ADDR, self.OLAT0, self.olat0)
        if self.active:
            self.olat1 = 0x00
        else:
            self.olat1 = 0xFF
        self.bus.write_byte_data(self.ADDR, self.OLAT1, self.olat1)

    def pinRead(self, group, pin):
        if group == 1:
            busVal = self.bus.read_byte_data(self.ADDR, self.GP1)
            self.olat1 = busVal
            state = ((busVal & (1 << pin)) != 0)
        else:
            busVal = self.bus.read_byte_data(self.ADDR, self.GP0)
            self.olat0 = busVal
            state = ((busVal & ( 1<< pin)) != 0)
        return state

    def setIPOL(self, group, pin):
        if group == 1:
            self.ipol1 = self.ipol1 | (1 << pin)
            self.bus.write_byte_data(self.ADDR, self.IPOL1, self.ipol1)
        else:
            self.ipol0 = self.ipol0 | (1 << pin)
            self.bus.write_byte_data(self.ADDR, self.IPOL0, self.ipol0)

    def resetIPOL(self, group, pin):
        if group == 1:
            self.ipol1 = self.ipol1 & (0xff - (1 << pin))
            self.bus.write_byte_data(self.ADDR, self.IPOLB, self.ipol1)
        else:
            self.ipol0 = self.ipol0 & (0xff - (1 << pin))
            self.bus.write_byte_data(self.ADDR, self.IPOL0, self.ipol0)

    def setGP(self, group, bitmask):
        """
        Set whole group of pins using bitmask. Warning: Set pins as output (using IODIR0/1) first!!
        group: 0, 1
        bitmask: 8bits, 0 -- turn off pin, 1--turn on pin
        """
        if group == 1:
            self.gp1 = bitmask
            self.bus.write_byte_data(self.ADDR, self.GP1, self.gp1)
        else:
            self.gp0 = bitmask
            self.bus.write_byte_data(self.ADDR, self.GP0, self.gp0)

    def resetGP(self, group, pin):
        if group == 1:
            self.gp1 = self.gp1 & (0xff - (1 << pin))
            self.bus.write_byte_data(self.ADDR, self.GP1, self.gp1)
        else:
            self.gp0 = self.gp0 & (0xff - (1 << pin))
            self.bus.write_byte_data(self.ADDR, self.GP0, self.gp0)

    def readINTCAP(self):
        busVal1 = self.bus.read_byte_data(self.ADDR, self.INTCAP0)
        busVal2 = self.bus.read_byte_data(self.ADDR, self.INTCAP1)
        return busVal1, busVal2

    def close(self):
        self.bus.close()

