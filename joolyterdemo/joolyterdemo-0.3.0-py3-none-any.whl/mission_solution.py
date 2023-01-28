"""Contains sample solutions for missions.
"""
import math
import joolyterdemo


def one():
    """Sample solution for Mission One: Hohmann Transfer
    """
    # given
    a1 = r1 = 750  # km
    mu = 3531.6  # km^3/s^2
    r = 600  # km
    h3 = 550  # km
    a3 = r3 = r + h3  # km

    # orbital velocity on parking orbit
    v1 = math.sqrt(mu / a1)  # km/s

    # semi-major axis of transfer orbit
    a2 = (r1 + r3) / 2  # km

    # orbital velocity on transfer orbit in pericenter
    v2_pe = math.sqrt(mu * (2 / r1 - 1 / a2))  # km/s

    # change of velocity to enter transfer orbit
    dv12 = v2_pe - v1  # km/s
    print("dv12 =", round(dv12, 3), "km/s")

    # orbital velocity on transfer orbit in apocenter
    v2_ap = math.sqrt(mu * (2 / r3 - 1 / a2))  # km/s

    # orbital velocity on target orbit
    v3 = math.sqrt(mu / a3)  # km/s

    # change of velocity to enter target orbit
    dv23 = v3 - v2_ap  # km/s
    print("dv23 =", round(dv23, 3), "km/s")

    # total of change of velocity
    dv_tot = dv12 + dv23  # km/s
    print("dv_tot =", round(dv_tot, 3), "km/s")

    # feed results to vessel/auto pilot
    joolyterdemo.Mission.one(dv12, dv23, dv_tot, "km/s")


def two():
    """Sample solution for Mission Two: Inclination Change
    """
    # given
    mu = 3531.6  # km^3/s^2
    a1 = r1 = 750  # km
    i1 = math.radians(7)  # rad
    day = 5 * 60 * 60 + 59 * 60 + 7  # s

    # orbital velocity in parking orbit
    v1 = math.sqrt(mu / a1)  # km/s

    # inclination change to reach target orbit
    di = 0 - i1  # rad

    # semi-major axis of target orbit from orbital period = day
    orb_period = day  # rad
    a3 = r3 = ((orb_period / (2 * math.pi)) ** 2 * mu) ** (1 / 3)  # km

    # semi-major axis of transfer orbit
    a2 = (r1 + r3) / 2  # km

    # orbital velocity on transfer orbit in pericenter
    v2_pe = math.sqrt(mu * (2 / r1 - 1 / a2))  # km/s

    # orbital velocity on transfer orbit in apocenter
    v2_ap = math.sqrt(mu * (2 / r3 - 1 / a2))  # km/s

    # orbital velocity in target orbit
    v3 = math.sqrt(mu / a3)  # km/s

    #################################################################################
    # OPTION 1
    # a) inclination-only change
    # b) traditional Hohmann-transfer
    #################################################################################
    # change in velocity for inclination change
    dv_incl = 2 * v1 * math.sin(di / 2)

    # change of velocity to enter transfer orbit
    dv12 = v2_pe - v1  # km/s

    # change of velocity to enter target orbit
    dv23 = v3 - v2_ap  # km/s

    # total change of velocity needed for option 1clear
    dv_tot_opt1 = abs(dv_incl) + dv12 + dv23  # km/s
    print("dv_tot_opt1 =", dv_tot_opt1)

    #################################################################################
    # OPTION 2
    # a) combined maneuver in pericenter of transfer orbit
    # b) in-plane burn to enter target orbit
    #################################################################################
    # change in velocity for combined inclination change in pericenter of transfer orbit
    dv12_opt2 = math.sqrt(v1**2 + v2_pe**2 - 2 * v1 * v2_pe * math.cos(di))

    # total change of velocity needed for option 2
    dv_tot_opt2 = dv12_opt2 + dv23  # km/s
    print("dv_tot_opt2 =", dv_tot_opt2)

    #################################################################################
    # OPTION 3
    # a) in-plane maneuver to enter transfer orbit
    # b) combined maneuver to enter target orbit
    #################################################################################
    # change in velocity for combined inclination change in apocenter of transfer orbit
    dv23_opt3 = math.sqrt(v2_ap**2 + v3**2 - 2 * v2_ap * v3 * math.cos(di))  # km/s

    # total change of velocity needed for option 3
    dv_tot_opt3 = dv12 + dv23_opt3  # km/sm
    print("dv_tot_opt3 =", dv_tot_opt3)

    #################################################################################
    # COMPARISON
    #################################################################################
    # find minimal change of velocity
    if dv_tot_opt1 < dv_tot_opt2 and dv_tot_opt1 < dv_tot_opt3:
        maneuver1 = joolyterdemo.InclinationChangeManeuver(dv_incl, v1, "km/s")
        maneuver2 = joolyterdemo.VelocityChangeManeuver(dv12, "km/s")
        maneuver3 = joolyterdemo.VelocityChangeManeuver(dv23, "km/s")
        option = 1
    elif dv_tot_opt2 < dv_tot_opt1 and dv_tot_opt2 < dv_tot_opt3:
        maneuver1 = joolyterdemo.CombinedManeuver(dv12_opt2, v1, v2_pe, "km/s")
        maneuver2 = joolyterdemo.VelocityChangeManeuver(dv23, "km/s")
        option = 2
    elif dv_tot_opt3 < dv_tot_opt1 and dv_tot_opt3 < dv_tot_opt2:
        maneuver1 = joolyterdemo.VelocityChangeManeuver(dv12, "km/s")
        maneuver2 = joolyterdemo.CombinedManeuver(dv23_opt3, v2_ap, v3, "km/s")
        option = 3
    else:
        raise ValueError("No unambiguous solution found.")

    print("Option", option, "is executed.")

    # feed results to vessel/auto pilot
    if option == 1 and 'maneuver3' in locals():
        joolyterdemo.Mission.two(maneuver1, maneuver2, maneuver3)
    else:
        joolyterdemo.Mission.two(maneuver1, maneuver2)
