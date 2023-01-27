""" This module provides common fuctions used in the computation of
    NESZ, AASR and RASR
"""

import os
import matplotlib
import numpy as np
import scipy.interpolate as interpol
from matplotlib import pyplot as plt

import drama.constants as cnst
import drama.geo as geo
import drama.utils as trtls
from .antenna_patterns import pattern
from drama.geo.geo_history import GeoHistory
from drama.io import cfg
from drama.utils.misc import save_object, load_object

def mode_from_conf(conf, modename="stripmap"):
    """

    Parameters
    ----------
    conf :

    modename :
         (Default value = 'stripmap')

    Returns
    -------

    """
    try:
        mcnf = getattr(conf, modename)
        # inc
        incs = np.zeros((mcnf.inc_near.size, 2))
        incs[:, 0] = mcnf.inc_near
        incs[:, 1] = mcnf.inc_far
        PRFs = mcnf.PRF
        proc_bw = mcnf.proc_bw
        steering_rate = np.zeros(incs.shape[0])
        steering_rate[:] = np.radians(mcnf.steering_rate)
        burst_length = np.ones_like(steering_rate)
        burst_length[:] = mcnf.burst_length
        short_name = mcnf.short_name
        proc_tap = np.ones_like(steering_rate)
        pulse_length = mcnf.pulse_length
        pulse_bw = mcnf.pulse_bw
        if hasattr(mcnf, "proc_tapering"):
            proc_tap[:] = mcnf.proc_tapering
        return (
            incs,
            PRFs,
            proc_bw,
            steering_rate,
            burst_length,
            short_name,
            proc_tap,
            pulse_length,
            pulse_bw,
        )
    except:
        mesg = "Mode %s is not defined" % modename
        raise ValueError(mesg)


def is_scansar(conf, modename="stripmap"):
    """ Checks if scansar mode, defaulting to False if paramters not defined """
    try:
        mcnf = getattr(conf, modename)
        if mcnf.scansar:
            iscnsr = True
        else:
            iscnsr = False
    except:
        iscnsr = False
    return iscnsr


def beamcentertime_to_zeroDopplertime(bct, steering_rate, dudt):
    """Computes the zero Doppler time from the beamcenter and the steering rate

    Parameters
    ----------
    """
    # t_bc = - steering_rate * t_in_b / (dudt - steering_rate)
    # if steering_rate == 0:
    #     # FIXME: no squint considered here!!!
    #     zdt = bct
    # else:
    #     #zdt = - bct * (dudt - steering_rate) / steering_rate
    zdt = bct * (1 - steering_rate / dudt)
    return zdt


def define_tx_ant(conf, txname, modename, swth, la_v, Tanalysis, info):
    """Creates the tx antenna pattern object

    Args:
        conf (_type_): object containing SAR configuration
        txname (str): Name of tx in configuration file
        modename (str): Name of mode, which should correspond to as section in cfg file
        swth (int): sub-swath number, starting at 0
        la_v (np.ndarray): array of look angles 
        Tanalysis (float): Time span analyzed, this is relevant to pre-compute the patterns
        info (obj): object for logging

    Returns:
        pattern: pattern object
    """

    # retrieve relevant sections of configuration   
    txcnf = getattr(conf, txname)
    mcnf = getattr(conf, modename)
    (
        incs,
        PRFs,
        proc_bw,
        steering_rates,
        burst_lengths,
        short_name,
        proc_tap,
        tau_p,
        bw_p,
    ) = mode_from_conf(conf, modename)
    if hasattr(txcnf, "wa_tx"):
        wa_tx = txcnf.wa_tx
    else:
        wa_tx = 1
    if hasattr(txcnf, "we_tx"):
        we_tx = txcnf.we_tx
    else:
        we_tx = 1
    tx_az_phase_attr = "wa_tx_phase_%i" % int(swth + 1)
    tx_el_phase_attr = "we_tx_phase_%i" % int(swth + 1)
    
    if hasattr(mcnf, tx_el_phase_attr):
        we_tx = np.exp(1j * np.radians(getattr(mcnf, tx_el_phase_attr)))
        # print(np.angle(we_tx))
        info.msg(
            "calc_nesz: applying elevation weighting to tx pattern!", 1
        )
        el0 = 0  # Pointing given in phase!
    else:
        we_tx = 1
        el0 = np.degrees(np.mean(la_v)) - txcnf.tilt
    # PLD 20220114 Adding code for azimuth beam spoiling
    if hasattr(mcnf, tx_az_phase_attr):
        info.msg("Applying azimuth phase spoiling. This will probably not work with azimuth steeing modes", 1)
        wa_tx = np.exp(1j * np.radians(getattr(mcnf, tx_az_phase_attr)))
        # print(np.angle(we_tx))

        az0 = 0  # Pointing given in phase!
    if hasattr(txcnf, "element_pattern"):
        if type(txcnf.element_pattern) == list:
            rel_ant = []
            for elcnf__ in txcnf.element_pattern:
                elcnf_ = getattr(conf, elcnf__)
                el_ant_ = pattern(conf.sar.f0,
                                    type_a=elcnf_.type_a,
                                    type_e=elcnf_.type_e,
                                    La=elcnf_.La,
                                    Le=elcnf_.Le,
                                    el0=(np.degrees(np.mean(la_v)) - elcnf_.tilt),
                                    Nel_a=elcnf_.Na,
                                    Nel_e=elcnf_.Ne,
                                    wa=elcnf_.wa_tx,
                                    we=elcnf_.we_tx,
                                    steering_rate=steering_rates[swth],
                                    Tanalysis=Tanalysis)
                el_ant.append(el_ant_)
        else:
            elcnf = getattr(conf, txcnf.element_pattern)
            el_ant = pattern(conf.sar.f0,
                                type_a=elcnf.type_a,
                                type_e=elcnf.type_e,
                                La=elcnf.La,
                                Le=elcnf.Le,
                                el0=(np.degrees(np.mean(la_v)) - elcnf.tilt),
                                Nel_a=elcnf.Na,
                                Nel_e=elcnf.Ne,
                                wa=elcnf.wa_tx,
                                we=elcnf.we_tx,
                                steering_rate=steering_rates[swth],
                                Tanalysis=Tanalysis)
    else:
        el_ant = None
    tx_ant = pattern(
        conf.sar.f0,
        type_a=txcnf.type_a,
        type_e=txcnf.type_e,
        La=txcnf.La,
        Le=txcnf.Le,
        el0=el0,
        Nel_a=txcnf.Na,
        Nel_e=txcnf.Ne,
        wa=wa_tx,
        we=we_tx,
        steering_rate=steering_rates[swth],
        Tanalysis=Tanalysis,
        element_pattern=el_ant,
    )
    return tx_ant


def define_rx_ant(conf, txname, rxname, modename, swth, bistatic, la_v, Tanalysis, info):
    """Creates the tx antenna pattern object

    Args:
        conf (_type_): object containing SAR configuration
        txname (str): Name of tx in configuration file
        modename (str): Name of mode, which should correspond to as section in cfg file
        swth (int): sub-swath number, starting at 0
        bistatic (bool): 
        la_v (np.ndarray): array of look angles 
        Tanalysis (float): Time span analyzed, this is relevant to pre-compute the patterns
        info (obj): object for logging

    Returns:
        pattern: pattern object
    """
    txcnf = getattr(conf, txname)
    rxcnf = getattr(conf, rxname)
    mcnf = getattr(conf, modename)
    (
        incs,
        PRFs,
        proc_bw,
        steering_rates,
        burst_lengths,
        short_name,
        proc_tap,
        tau_p,
        bw_p,
    ) = mode_from_conf(conf, modename)
    if hasattr(rxcnf, "wa_rx"):
        if type(rxcnf.wa_rx) is np.ndarray:
            wa_rx = rxcnf.wa_rx
        else:
            c0 = rxcnf.wa_rx
            Na = rxcnf.Na
            wa_rx = c0 - (1 - c0) * np.cos(
                2 * np.pi * np.arange(Na) / (Na - 1)
            )
    else:
        wa_rx = 1
    if hasattr(mcnf, "we_rx"):
        # Do something
        c0 = mcnf.we_rx[swth]
        Ne = rxcnf.Ne
        we_rx = c0 - (1 - c0) * np.cos(2 * np.pi * np.arange(Ne) / (Ne - 1))
    elif hasattr(rxcnf, "we_rx"):
        if type(rxcnf.we_rx) is np.ndarray:
            we_rx = rxcnf.we_rx
        else:
            c0 = rxcnf.we_rx
            Ne = rxcnf.Ne
            we_rx = c0 - (1 - c0) * np.cos(
                2 * np.pi * np.arange(Ne) / (Ne - 1)
            )
    else:
        we_rx = 1

    if hasattr(rxcnf, "azimuth_spacing"):
        azimuth_spacing = rxcnf.azimuth_spacing
    else:
        azimuth_spacing = 1
    if hasattr(rxcnf, "elevation_spacing"):
        elevation_spacing = rxcnf.elevation_spacing
    else:
        elevation_spacing = 1
    if bistatic:
        # FIX-ME
        rx_el0 = (
            0
        )  # because we do optimal pointing, which is not totally fair for burst modes
    else:
        rx_el0 = np.degrees(np.mean(la_v)) - txcnf.tilt

    # Elevation phase spoiling
    rx_el_phase_attr = "we_rx_phase_%i" % int(swth + 1)
    if hasattr(mcnf, rx_el_phase_attr):
        we_rx = we_rx * np.exp(1j * np.radians(getattr(mcnf, tx_el_phase_attr)))
        print(np.angle(we_rx))
        info.msg(
            "calc_nesz: applying elevation weighting to rx pattern!", 1
        )
        rx_el0 = 0  # Pointing given in phase! 
    if hasattr(rxcnf, "element_pattern"):
        info.msg("Initializing element pattern")

        if type(rxcnf.element_pattern) == list:
            rel_ant = []
            for elcnf__ in rxcnf.element_pattern:
                elcnf_ = getattr(conf, elcnf__)
                rel_ant_ = pattern(conf.sar.f0,
                                    type_a=elcnf_.type_a,
                                    type_e=elcnf_.type_e,
                                    La=elcnf_.La,
                                    Le=elcnf_.Le,
                                    el0=rx_el0,
                                    Nel_a=elcnf_.Na,
                                    Nel_e=elcnf_.Ne,
                                    wa=elcnf_.wa_rx,
                                    we=elcnf_.we_rx,
                                    steering_rate=steering_rates[swth],
                                    Tanalysis=Tanalysis)
                rel_ant.append(rel_ant_)
        else:
            elcnf = getattr(conf, rxcnf.element_pattern)
            rel_ant = pattern(conf.sar.f0,
                                type_a=elcnf.type_a,
                                type_e=elcnf.type_e,
                                La=elcnf.La,
                                Le=elcnf.Le,
                                el0=rx_el0,
                                Nel_a=elcnf.Na,
                                Nel_e=elcnf.Ne,
                                wa=elcnf.wa_rx,
                                we=elcnf.we_rx,
                                steering_rate=steering_rates[swth],
                                Tanalysis=Tanalysis)
    else:
        rel_ant = None
    rx_ant = pattern(
        conf.sar.f0,
        type_a=rxcnf.type_a,
        type_e=rxcnf.type_e,
        La=rxcnf.La,
        Le=rxcnf.Le,
        el0=rx_el0,
        Nel_a=rxcnf.Na,
        Nel_e=rxcnf.Ne,
        wa=wa_rx,
        we=we_rx,
        steering_rate=steering_rates[swth],
        Tanalysis=Tanalysis,
        spacing_a=azimuth_spacing,
        spacing_e=elevation_spacing,
        element_pattern=rel_ant,
    )
    return rx_ant


def plot_pattern(
    tv,
    t_bc,
    ddop,
    tx_pat,
    rx_pat,
    tw_pat,
    tw_pat_amb,
    tw_sumpat_amb,
    proc_bw,
    n_amb,
    title,
    savefile,
    lat_ind=25,
    making_off=False,
    t_span=2,
):
    """

    Parameters
    ----------
    lat_ind :
         (Default value = 25)
    making_off :
         (Default value = False)
    t_span :
         (Default value = 2)

    Returns
    -------

    """
    # lat_ind = 25
    goodf = np.where(np.abs(ddop[lat_ind]) < proc_bw / 2)
    plt.figure()
    plt.plot(tv, trtls.db(np.abs(tx_pat[lat_ind]) ** 2), label="$G_{tx}$")
    plt.xlabel("Integration window [s]")
    plt.ylabel("G [dB]")
    plt.ylim(-40, 3)
    plt.xlim(-t_span / 2 + t_bc[lat_ind], t_span / 2 + t_bc[lat_ind])
    plt.title(title)
    plt.grid(True)
    os.makedirs(os.path.dirname(savefile), exist_ok=True)
    if making_off:
        svfl = (
            os.path.splitext(savefile)[0]
            + "_p1."
            + os.path.splitext(savefile)[1]
        )
        plt.savefig(svfl, bbox_inches="tight")

    plt.plot(tv, trtls.db(np.abs(rx_pat[lat_ind]) ** 2), label="$G_{rx}$")
    if making_off:
        svfl = (
            os.path.splitext(savefile)[0]
            + "_p2."
            + os.path.splitext(savefile)[1]
        )
        plt.savefig(svfl, bbox_inches="tight")

    plt.plot(tv, trtls.db(tw_pat[lat_ind]), "g", lw=1)
    plt.plot(
        tv[goodf], trtls.db(tw_pat[lat_ind][goodf]), "g", label="$G_{2w}$", lw=3
    )
    if making_off:
        svfl = (
            os.path.splitext(savefile)[0]
            + "_p3."
            + os.path.splitext(savefile)[1]
        )
        plt.savefig(svfl, bbox_inches="tight")

    for ind in range(2 * n_amb):
        plt.plot(tv, (trtls.db(tw_pat_amb[lat_ind, ind])), "--", lw=1)
        if making_off:
            svfl = (
                os.path.splitext(savefile)[0]
                + ("_p%i." % (int(4 + ind)))
                + os.path.splitext(savefile)[1]
            )
            plt.savefig(svfl, bbox_inches="tight")

    plt.plot(tv, (trtls.db(tw_sumpat_amb[lat_ind])), "r", lw=1)
    plt.plot(
        tv[goodf],
        (trtls.db(tw_sumpat_amb[lat_ind][goodf])),
        "r",
        lw=3,
        label="$\sum G_{2w,a}$ ",
    )

    plt.legend()

    plt.savefig(savefile, bbox_inches="tight")
