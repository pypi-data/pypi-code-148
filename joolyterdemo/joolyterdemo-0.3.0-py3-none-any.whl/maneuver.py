"""Contains classes for maneuver types.

Classes:
    * ImpulseManeuver: Base class - not supposed to be called. Contains general information for maneuver and function to compute directional dv.
    * VelocityChange (BaseClass): Represents maneuver in orbital plane changing only orbital velocity.
    * InclinationChange (BaseClass): Represents maneuver changing inclination w/o changes of orbital velocity.
    * Combined (BaseClass): Represents maneuver changing inclination of orbital plane and orbital velocity.
"""

import math
from typing import Tuple


class ImpulseManeuver:
    """Base class for different maneuver types. Not supposed to be called directly.

    :param dv: Change in velocity for maneuver
    :type dv: float
    :param unit: Unit of provided velocity values, defaults to "m/s"
    :type unit: str, optional
    :raises ValueError: Is raised if unit is not "m/s" or "km/s"
    """
    def __init__(self, dv: float, unit: str = 'm/s') -> None:
        """Constructs and calculates all necessary attributes

        :raises ValueError: Is raised if wrong unit is given
        """
        if unit == 'km/s':
            self.dv = dv * 1000
        elif unit == 'm/s':
            self.dv = dv
        else:
            raise ValueError(
                "Unit unknown! Default unit is 'm/s'. "
                "If unit is provided make sure it is 'm/s' or 'km/s'."
            )

        self._burn_angle = .0  # rad

    def direct_dv(self) -> Tuple[float, float, float]:
        """Computes directional dv as tuple from class instance's dv and _burn_angle

        :return: dv in 3D-tuple: (dv_radial, dv_prograde, dv_normal)
        :rtype: Tuple[float, float, float]
        """
        dv_pro = self.dv * math.cos(self._burn_angle)
        dv_normal = self.dv * math.sin(self._burn_angle)
        return 0, dv_pro, dv_normal

    def invert_burn_angle(self) -> None:
        """Inverts private field _burn_angle
        """
        self._burn_angle *= -1


class VelocityChangeManeuver(ImpulseManeuver):
    """Representing in orbital plane maneuvers / solely energetic change

    :param dv: Change in velocity for maneuver
    :type dv: float
    :param unit: Unit of provided velocity values, defaults to "m/s"
    :type unit: str, optional
    :raises ValueError: Is raised if unit is not "m/s" or "km/s"
    """

    def __init__(self, dv: float, unit: str = 'm/s') -> None:
        """Constructs and calculates all necessary attributes

        :raises ValueError: Is raised if wrong unit is given
        """
        super().__init__(dv, unit)


class InclinationChangeManeuver(ImpulseManeuver):
    """Representing maneuvers only changing inclination / without energetic change.

    :param dv: Change in velocity for maneuver
    :type dv: float
    :param v: Orbital velocity at maneuver
    :type v: float
    :param unit: Unit of provided velocity values, defaults to 'm/s'
    :type unit: str, optional
    :raises ValueError: Is raised if unit is not "m/s" or "km/s"
    """
    def __init__(self, dv: float, v: float, unit: str = 'm/s') -> None:
        """Constructs and calculates all necessary attributes

        :raises ValueError: Is raised if wrong unit is given
        """
        if unit == 'km/s':
            self.dv = dv * 1000
            self.v = v * 1000
        elif unit == 'm/s':
            self.dv = dv
            self.v = v
        else:
            raise ValueError(
                "Unit unknown! Default unit is 'm/s'. "
                "If unit is provided make sure it is 'm/s' or 'km/s'."
            )

        self._burn_angle = math.radians(180) - math.acos(dv / 2 * v)  # law of cosines for v1 = v2 = v


class CombinedManeuver(ImpulseManeuver):
    """Representing combined maneuvers changing inclination and velocity

    :param dv: Change in velocity for maneuver
    :type dv: float
    :param v1: Orbital velocity before maneuver
    :type v1: float
    :param v2: Orbital velocity after maneuver
    :type v2: float
    :param unit: Unit of provided velocity values, defaults to 'm/s'
    :type unit: str, optional
    :raises ValueError: Is raised if unit is not "m/s" or "km/s"
    """
    def __init__(
            self, dv: float, v1: float, v2: float, unit: str = 'm/s'
    ) -> None:
        """Constructs and calculates all necessary attributes

        :raises ValueError: Is raised if wrong unit is given
        """
        if unit == 'km/s':
            self.dv = dv * 1000
            self.v1 = v1 * 1000
            self.v2 = v2 * 1000
        elif unit == 'm/s':
            self.dv = dv
            self.v1 = v1
            self.v2 = v2
        else:
            raise ValueError(
                "Unit unknown! Default unit is 'm/s'. "
                "If unit is provided make sure it is 'm/s' or 'km/s'."
            )

        x = (dv**2 + v1**2 - v2**2) / (2 * dv * v1)
        if -1 <= x <= 1:
            self._burn_angle = math.radians(180) - math.acos(x)  # law of cosines
        else:
            raise ValueError(
                "math domain error. [arccos(x) is defined for -1 <= x <= 1]"
            )
