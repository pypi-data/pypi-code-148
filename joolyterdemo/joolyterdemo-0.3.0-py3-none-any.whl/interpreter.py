"""
Contains logic to interpret user input for demo mission one and tow.

Functions:
    * one (dv12: float, dv23: float, dvtot: float, unit: str = "m/s") -> bool: Returns True if mission was successful.
    * two(maneuver1: functions.ImpulseManeuver, maneuver2: functions.Maneuver, maneuver3: functions.Maneuver = None, unit = "m/s") -> bool: Returns True if mission was successful.
"""
from joolyterdemo.maneuver import ImpulseManeuver
from joolyterdemo.functions import Setup
import math


class Mission:
    def __init__(self, name: str) -> None:
        self.name = name

    @staticmethod
    def one(
        dv12: float,
        dv23: float,
        unit: str = 'm/s'
    ) -> bool:
        """Commands KSP to perform burns with provided changes of velocity

        :param dv12: Change of velocity to put vessel into transfer orbit
        :type dv12: float
        :param dv23: Change of velocity to put vessel into target orbit
        :type dv23: float
        :param unit: Unit of provided parameters, defaults to 'm/s'
        :type unit: str, optional
        :raises ValueError: Is raised if wrong unit is given
        :return: True if target orbit is reached (within margin)
        :rtype: bool
        """

        # mission objectives
        r_target = 1150000  # m
        r_margin = 1000  # m
        incl_target = math.radians(28.45)  # rad
        incl_margin = 0.05

        # unit check
        if unit == 'km/s':
            dv12 = dv12 * 1000
            dv23 = dv23 * 1000
        elif unit != 'm/s':
            raise ValueError(
                "Unit unknown! Default unit is 'm/s'."
                "If unit is provided make sure it is 'm/s' or 'km/s'."
            )
        else:
            pass

        # setup server client and streams
        setup_one = Setup("Mission One - Hohmann-Transfer")

        # activate first stage
        setup_one.next_stage()

        # set first maneuver in 90 s
        t_maneuver12 = setup_one.ut + 90

        # perform first maneuver
        setup_one.impulse_maneuver(t_maneuver=t_maneuver12, dv_pro=dv12)

        # [optional - disabled]
        # check and return if maneuver was not successful
        # if ap < r_target - r_margin or ap > r_target + r_margin:
        #     return False

        # calculate details for circularization burn
        t_maneuver23 = setup_one.ut + setup_one.t_to_ap

        setup_one.impulse_maneuver(t_maneuver=t_maneuver23, dv_pro=dv23)

        # check and return bool if maneuver was successful
        if (
            setup_one.ap < r_target - r_margin
            or setup_one.ap > r_target + r_margin
            or setup_one.pe < r_target - r_margin
            or setup_one.pe > r_target + r_margin
            or setup_one.incl < incl_target * (1 - incl_margin)
            or setup_one.incl > incl_target * (1 + incl_margin)
        ):
            return False
        else:
            return True

    @staticmethod
    def two(
        maneuver1: ImpulseManeuver,
        maneuver2: ImpulseManeuver,
        maneuver3: ImpulseManeuver = None
    ) -> bool:
        """Commands KSP to perform specified types of maneuvers with provided changes of velocity

        :param maneuver1: First maneuver to perform
        :type maneuver1: ImpulseManeuver
        :param maneuver2: Second maneuver to perform
        :type maneuver2: ImpulseManeuver
        :param maneuver3: Third maneuver to perform, defaults to None
        :type maneuver3: ImpulseManeuver, optional
        :raises ValueError: Is raised if line of nodes does not coincide with apsides
        :return: True if "kerbisynchronous" orbit is reached (within margin).
        :rtype: bool
        """
        # mission objectives (kRPC does not cover access to mission goals)
        r_target = 3463074  # m
        r_margin = 15000  # m
        incl_target = 0  # rad
        incl_margin = math.radians(0.5)

        # setup server client and streams by instantiating Setup class
        setup_two = Setup("Mission Two - Inclination Change")

        # activate first stage
        # TODO: Delete here or in Mission Builder
        setup_two.next_stage()

        # store maneuvers in list for easier processing
        maneuver_list = [maneuver1, maneuver2, maneuver3]

        # processing loop
        for maneuver_i in maneuver_list:
            if maneuver_i is not None:
                # get time to ascending (AN) or descending (DN) nodes
                t_to_an = setup_two.t_to_node()
                t_to_dn = setup_two.t_to_node('dn')
                # check if apsides coincide with line of nodes by comparing time delta
                # comparison values (45 s at ap and 5 s at pe) educated guesses and will need extensive 
                # testing on more machines
                if setup_two.ecc > 0.00133 and (
                    (
                        abs(t_to_an - setup_two.t_to_ap)
                        or abs(t_to_dn - setup_two.t_to_ap) > 45
                    )
                    and (
                        abs(t_to_an - setup_two.t_to_pe)
                        or abs(t_to_dn - setup_two.t_to_pe) > 5
                    )
                ):
                    raise ValueError(
                        "Line of nodes does not coincide with apsides."
                        "Please contact support!"
                    )
                # check for nearest node
                if t_to_an <= t_to_dn:
                    t_maneuver = t_to_an + setup_two.ut
                    maneuver_i.invert_burn_angle()
                else:
                    t_maneuver = t_to_dn + setup_two.ut
                # perform burn
                dv_rad, dv_pro, dv_norm = maneuver_i.direct_dv()
                setup_two.impulse_maneuver(t_maneuver, dv_pro, dv_norm)
            else:
                pass

        # check and return bool if maneuver was successful
        if (
            setup_two.ap < r_target - r_margin
            or setup_two.ap > r_target + r_margin
            or setup_two.pe < r_target - r_margin
            or setup_two.pe > r_target + r_margin
            or setup_two.incl < incl_target * (1 - incl_margin)
            or setup_two.incl > incl_target * (1 + incl_margin)
        ):
            return False
        else:
            return True
