#  Copyright (c) 2023 ETH Zurich, SIS ID and HVL D-ITET
#
"""
EarhtingStick of the different "Cubes".
"""
import logging
from typing import TYPE_CHECKING

from aenum import IntEnum

from hvl_ccb.utils.enum import BoolEnum

from .constants import SafetyStatus
from .errors import CubeEarthingStickOperationError

if TYPE_CHECKING:
    from . import BaseCube  # pragma: no cover

logger = logging.getLogger(__name__)


class EarthingStickStatus(IntEnum):
    """
    Status of an earthing stick. These are the possible values in the status integer
    e.g. in :attr:`_EarthingStick.status`.
    """

    # Earthing stick is deselected and not enabled in safety circuit. To get out of
    # this state, the earthing has to be enabled in the BaseCube HMI setup.
    INACTIVE = 0

    # Earthing is closed (safe).
    CLOSED = 1

    # Earthing is open (not safe).
    OPEN = 2

    # Earthing is in error, e.g. when the stick did not close correctly or could not
    # open.
    ERROR = 3


class EarthingStickOperatingStatus(IntEnum):
    """
    Operating Status for an earthing stick. Stick can be used in auto or manual mode.
    """

    AUTO = 0
    MANUAL = 1


class EarthingStickOperation(BoolEnum):
    """
    Operation of the earthing stick in manual operating mode. Can be closed of opened.
    """

    OPEN = False
    CLOSE = True


class _EarthingStick:
    """
    Earthing sticks with status, operating status (manual and auto) and manual operate.
    """

    _STICKS: tuple = (1, 2, 3, 4, 5, 6)

    def __init__(self, handle, number: int):
        self._handle: BaseCube = handle
        self._number: int = number
        self._CMD_STATUS: str = (
            f'"DB_Safety_Circuit"."Earthstick_{number}"."si_HMI_Status"'
        )
        self._CMD_OPERATING_STATUS: str = (
            f'"DB_Safety_Circuit"."Earthstick_{number}"."sx_manual_control_active"'
        )
        self._CMD_MANUAL: str = (
            f'"DB_Safety_Circuit"."Earthstick_{number}"."sx_earthing_manually"'
        )

    @property
    def status(self) -> EarthingStickStatus:
        """
        Status of the earthing stick.

        :return: Status of the earthing stick.
        """
        value = EarthingStickStatus(self._handle.read(self._CMD_STATUS))
        logger.info(f"Status of Earthing Stick {self._number} is {value.name}")
        return value

    @property
    def operating_status(self) -> EarthingStickOperatingStatus:
        """
        Earthing stick operating status, if 'manual' the stick can be controlled by the
        user.

        :return: Earthing stick operating status, can be either auto or manual
        """
        value = EarthingStickOperatingStatus(
            self._handle.read(self._CMD_OPERATING_STATUS)
        )
        logger.info(
            f"Operating Status of Earthing Stick {self._number} is {value.name}"
        )
        return value

    @property
    def operate(self) -> EarthingStickOperation:
        """
        Operation of an earthing stick, which is set to manual operation.

        :return: Earthing stick operation status, can be open or close
        """
        value = EarthingStickOperation(self._handle.read(self._CMD_MANUAL))
        logger.info(f"Manual Status of Earthing Stick {self._number} is {value}")
        return value

    @operate.setter
    def operate(self, operation: EarthingStickOperation) -> None:
        """
        Operation of an earthing stick, which is set to manual operation. If an earthing
        stick is set to manual, it stays closed even if the system is in states
        RED_READY or RED_OPERATE.

        :param operation: earthing stick manual status (close or open)
        :raises CubeEarthingStickOperationError: when operating status of given
            number's earthing stick is not manual
        """
        operation = EarthingStickOperation(operation)
        if self._handle.status not in (
            SafetyStatus.RED_READY,
            SafetyStatus.RED_OPERATE,
        ):
            msg = (
                'Cube needs to be in state "RED_READY" or "RED_OPERATE" '
                "to operate Earthing Stick manually, "
                f'but is in "{self._handle.status.name}".'
            )
            logger.error(msg)
            raise CubeEarthingStickOperationError(msg)
        if self.operating_status == EarthingStickOperatingStatus.MANUAL:
            self._handle.write(self._CMD_MANUAL, operation)
            logger.info(f"Earthing Stick {self._number} is set to {operation}")
        else:
            msg = (
                f"Operation of the Earthing Stick {self._number} is not possible, "
                "as the feature is not activated in the Cube Setup."
            )
            logger.error(msg)
            raise CubeEarthingStickOperationError(msg)
