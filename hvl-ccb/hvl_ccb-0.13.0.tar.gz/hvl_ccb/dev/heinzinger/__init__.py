#  Copyright (c) 2019-2022 ETH Zurich, SIS ID and HVL D-ITET
#
"""
Device classes for Heinzinger Digital Interface I/II and Heinzinger PNC power supply.

The Heinzinger Digital Interface I/II is used for many Heinzinger power units.
Manufacturer homepage:
https://www.heinzinger.com/products/accessories-and-more/digital-interfaces/

The Heinzinger PNC series is a series of high voltage direct current power supplies.
The class HeinzingerPNC is tested with two PNChp 60000-1neg and a PNChp 1500-1neg.
Check the code carefully before using it with other PNC devices, especially PNC3p
or PNCcap.
Manufacturer homepage:
https://www.heinzinger.com/products/high-voltage/universal-high-voltage-power-supplies/
"""

from hvl_ccb.dev.heinzinger.base import (  # noqa: F401
    HeinzingerConfig,
    HeinzingerDI,
    HeinzingerPNC,
    HeinzingerSerialCommunication,
    HeinzingerSerialCommunicationConfig,
)
from hvl_ccb.dev.heinzinger.constants import (  # noqa: F401
    HeinzingerPNCDeviceNotRecognizedError,
    HeinzingerPNCError,
    HeinzingerPNCMaxCurrentExceededError,
    HeinzingerPNCMaxVoltageExceededError,
)
