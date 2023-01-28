"""Contains class that represents bundle of pre-built methods and properties
for quick access

Classes:
    * Setup: Base class for one client and one connected vessel
"""


import krpc
import math
import time
from typing import Tuple


class Setup:
    """Class containing pre-built functions

        :param name: Name of save game
        :type name: str
    """
    def __init__(self, name: str) -> None:
        """Constructs class with all necessary attributes
        """
        self.name = name
        # connect to KSP
        self._conn = krpc.connect(name=self.name)
        # connect to vessel
        self._vessel = self._conn.space_center.active_vessel
        # assign streams
        self._ut = self._conn.add_stream(
            getattr,
            self._conn.space_center,
            'ut'
        )  # s
        self._ap = self._conn.add_stream(
            getattr,
            self._vessel.orbit,
            'apoapsis'
        )  # m
        self._t_to_ap = self._conn.add_stream(
            getattr,
            self._vessel.orbit,
            'time_to_apoapsis'
        )  # s
        self._pe = self._conn.add_stream(
            getattr,
            self._vessel.orbit,
            'periapsis'
        )  # m
        self._t_to_pe = self._conn.add_stream(
            getattr,
            self._vessel.orbit,
            'time_to_periapsis'
        )  # s
        self._incl = self._conn.add_stream(
            getattr,
            self._vessel.orbit,
            'inclination'
        )  # rad
        self._ecc = self._conn.add_stream(
            getattr,
            self._vessel.orbit,
            'eccentricity'
        )
        self.print_current_state()

    @property
    def connection(self) -> krpc.Client:
        """Client of instance

        :return: Active connection
        :rtype: krpc.Client
        """
        return self._conn

    @property
    def vessel(self) -> krpc.types.Vessel:
        """Connected vessel of instance

        :return: Connected active vessel
        :rtype: krpc.types.Vessel
        """
        return self._vessel

    @property
    def ut(self) -> int:
        """Universal time

        :return: Kerbin universal time in seconds
        :rtype: int
        """
        return self._ut()

    @property
    def ap(self) -> float:
        """Apoapsis (radius)

        :return: Radial value of apoapsis in meter
        :rtype: float
        """
        return self._ap()

    @property
    def t_to_ap(self) -> int:
        """Time to apoapsis

        :return: Time to apoapsis in seconds
        :rtype: int
        """
        return self._t_to_ap()

    @property
    def pe(self) -> float:
        """Periapsis (radius)

        :return: Radial value of periapsis in meter
        :rtype: float
        """
        return self._pe()

    @property
    def t_to_pe(self) -> int:
        """Time to periapsis

        :return: Time to periapsis in seconds
        :rtype: int
        """
        return self._t_to_pe()

    @property
    def incl(self) -> float:
        """Inclination of orbital plane of instance's orbit relative to
        equatorial plane orbiting body

        :return: Inclination in radians
        :rtype: float
        """
        return self._incl()

    @property
    def ecc(self) -> float:
        """Numerical eccentricity

        :return: Numerical eccentricity
        :rtype: float
        """
        return self._ecc()

    @staticmethod
    def calc_norm(t: Tuple[float, ...]) -> float:
        """Calculates norm of tuple of floats

        :param t: Tuple of floats
        :type t: Tuple[float, ...]
        :return: Norm of tuple
        :rtype: float
        """
        sigma = 0
        for i in t:
            sigma += i**2
        norm_t = math.sqrt(sigma)
        return norm_t

    def next_stage(self) -> None:
        """Activates next stage of connected active vessel.
        """
        self._vessel.control.activate_next_stage()

    def print_current_state(self) -> None:
        """Prints current state of active connected vessel.
        """
        body = self._vessel.orbit.body
        # print data
        print(
            "Link to",
            self._vessel.name,
            "was successfully established."
        )
        print(
            self._vessel.name,
            "is orbiting",
            body.name,
            "with a Periapsis altitude H_pe of",
            round(self._pe() - body.equatorial_radius) / 1000,
            "km and an Apoapsis altitude H_ap of",
            round(self._ap() - body.equatorial_radius) / 1000,
            "km and an inclination i of",
            round(math.degrees(self._incl()), 3),
            "°.",
        )

    def calc_dt_burn(self, dv: float) -> float:
        """Calculates duration burn requires for provided change of velocity
        for global instance of :type:'krpc.types.Vessel vessel'.

        :param dv: Change of velocity
        :type dv: float
        :return: Time vessel has to fire up its engines for in seconds
        :rtype: float
        """
        f = self._vessel.available_thrust
        g0 = self._vessel.orbit.body.surface_gravity
        c_e = self._vessel.specific_impulse * g0
        m0 = self._vessel.mass
        m1 = m0 / math.exp(dv / c_e)
        m_dot = f / c_e
        return (m0 - m1) / m_dot

    def impulse_maneuver(
        self,
        t_maneuver: int,
        dv_pro=0.0,
        dv_normal=0.0,
        dv_rad=0.0,
        lead_time=30
    ) -> bool:
        """Commands KSP to perform specified burn with provided changes of
        velocity for instance connected :type:'krpc.types.Vessel' vessel
        of instance of :class:'Setup' setup

        :param t_maneuver: Start of burn in universal time in seconds
        :type t_maneuver: int
        :param dv_pro: Change of velocity in prograde direction, defaults to 0.0
        :type dv_pro: float, optional
        :param dv_normal: Change of velocity in normal direction, defaults to 0.0
        :type dv_normal: float, optional
        :param dv_rad: Change of velocity in radial direction, defaults to 0.0
        :type dv_rad: float, optional
        :param lead_time: Duration time warp[inactive] stops before burn in seconds, defaults to 30
        :type lead_time: int, optional
        :raises ValueError: Is raised if method is called too late
        :return: True if burn is completely executed
        :rtype: bool
        """
        dv = (dv_rad, dv_pro, dv_normal)
        norm_dv = Setup.calc_norm(dv)
        if norm_dv == 0.0:
            return False
        dt_burn = self.calc_dt_burn(norm_dv)
        # checks if lead_time is complied by, to ensure vessel has enough time to turn
        if t_maneuver - self._ut() < lead_time:
            raise ValueError(
                "'burn'-method must be called at least",
                lead_time,
                "seconds before t_maneuver to setup. Try manually adjusting "
                "\'lead_time\' or call function earlier."
            )
        # add maneuver node
        node = self._vessel.control.add_node(
            t_maneuver, prograde=dv_pro, normal=dv_normal, radial=dv_rad
        )
        # orientate satellite to prograde (in coordinate system of maneuver node_12)
        self._vessel.auto_pilot.reference_frame = node.reference_frame
        self._vessel.auto_pilot.target_direction = (
            0,
            1,
            0,
        )  # in prograde direction in nodes ref. frame ("direction = nodes direction")
        time.sleep(3)
        self._vessel.auto_pilot.engage()
        print("Autopilot engaged.")
        time.sleep(3)
        self._vessel.auto_pilot.wait()
        print("Locked on to target direction.")
        time.sleep(4)
        print("Ready for maneuver.")

        # [optional - disabled]
        # wait for maneuver
        # if t_maneuver - self._ut - dt_burn/2 - lead_time > lead_time + 10:
        #     self._conn.space_center.warp_to(t_maneuver-lead_time)

        # wait to burn
        while t_maneuver - self._ut() - dt_burn / 2 > 0:
            time.sleep(0.01)
            pass
        # burn start
        self._vessel.control.throttle = 1.0
        # burn loop:
        # burn until tank of current stage is empty or
        # thrust is slowly reduced until no dv remains
        while (
            self._vessel.resources_in_decouple_stage(
                self._vessel.control.current_stage - 1
            ).amount('Oxidizer')
            > 0
        ):
            if node.remaining_delta_v <= 0.1:
                self._vessel.control.throttle = 0.0
                self._vessel.auto_pilot.disengage()
                break
            elif node.remaining_delta_v <= 1:
                self._vessel.control.throttle = 0.01
                pass
            elif node.remaining_delta_v <= 7:
                self._vessel.control.throttle = 0.1
                pass
            elif node.remaining_delta_v <= 15:
                self._vessel.control.throttle = 0.5
                pass
        # return True if maneuver is completed
        if (
            node.remaining_delta_v < 1.
            and self._vessel.resources_in_decouple_stage(
                self._vessel.control.current_stage - 1
            ).amount('Oxidizer')
            > 0
        ):
            node.remove()
            return True
        else:
            return False

    def t_to_node(
        self,
        node='an'
    ) -> int:
        """Calculates time to absolute ascending ['an'] or descending node ['dn']. Only works for Kerbin.

        :param node: Node to which time is calculated, defaults to 'an'
        :type node: str
        :return: Time to specified node in [s]
        :rtype: int
        """
        # there is no function to get time to ascending (AN) or descending (DN) node directly 
        # thus, true anomaly (TA) at AN and DN in relation to Mün's orbit is called and used 
        # to get UT at said TA. Current time is subtracted to get time delta.
        # currently works only for Kerbin. Would need different approach for other bodies.
        if(node is 'dn'):
            t_to_node = (
                self._vessel.orbit.ut_at_true_anomaly(
                    self._vessel.orbit.true_anomaly_at_dn(
                        self._vessel.orbit.body.satellites[0].orbit
                        )
                )
                - self.ut
            )
        else:
            t_to_node = (
                self._vessel.orbit.ut_at_true_anomaly(
                    self._vessel.orbit.true_anomaly_at_an(
                        self._vessel.orbit.body.satellites[0].orbit
                        )
                )
                - self.ut
            )
        return t_to_node
        