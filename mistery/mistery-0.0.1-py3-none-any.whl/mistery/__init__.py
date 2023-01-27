#!/usr/bin/env python3

import io
from urllib.request import urlopen
from zipfile import ZipFile
import requests
import numpy as np
import numpy.lib.recfunctions as rfn

BASE_URL = 'http://waps.cfa.harvard.edu/MIST/'

def get_track(M=1.0, **kwargs):
    """Returns a single evolutionary track from the MIST database with
    mass ``M`` (in solar units) and metallicity [Fe/H] ``FeH``.  The
    script makes the PHP request, infers the archive's filename,
    decompresses it, and returns a NumPy structured array.  You can
    get the list of column names with e.g.

        track = mistery.get_track(M=2.0, FeH=-0.5)
        print(track.dtype.names)

    """
    return get_tracks(Ms=[M], **kwargs)[0]


def get_tracks(Ms=[1.0], FeH=0.0, vvcrit=0.0, Av=0.0, output='theory'):
    """Returns a list of evolutionary tracks from the MIST database
    with masses ``Ms`` (iterable, in solar units) and metallicity
    [Fe/H] ``FeH``.  The script makes the PHP request, infers the
    archive's filename, decompresses it, and returns a list of NumPy
    structured arrays.  You can get the list of column names with e.g.

        tracks = mistery.get_track(Ms=[1.0, 2.0], FeH=-0.5)
        print(tracks[0].dtype.names)

    """
    # choosing a mass more precisely than 0.0001 Msun causes a variety of issues
    if any([np.abs(M-np.round(M, 4)) > 2*np.finfo(type(M)).resolution for M in Ms]):
        raise ValueError

    data = {
        'version': '1.2',
        'v_div_vcrit': 'vvcrit%.1f' % vvcrit,
        'mass_type': 'list',
        'mass_value': '',
        'mass_range_low': '',
        'mass_range_high': '',
        'mass_range_delta': '',
        'mass_list': ' '.join(['%g' % M for M in Ms]),
        'new_met_value': '%g' % FeH,
        'output_option': 'theory',
        'output': 'UBVRIplus',
        'Av_value': '%g' % Av
    }

    if output != 'theory':
        data['output_option'] = 'photometry'
        data['output'] = output

    r = requests.post(
        BASE_URL+'track_form.php',
        data=data
    )

    filename = r.text[18:48]

    # hacked together based on
    # https://stackoverflow.com/a/952834
    f = ZipFile(io.BytesIO(urlopen(BASE_URL + filename).read()))

    tracks = []
    for M in Ms:
        basename = './%07iM.track.eep' % np.round(M*1e4)
        track = np.genfromtxt(f.read(basename).decode().split('\n'),
                              skip_header=11, names=True, dtype=None)

        # if we request photometry, it's delivered in a separate file in the zip
        # so here we handle reading it alongside the relevant track
        # then joining the data by first dropping everything already in the track
        # then merging on star_age, which is the first column in both files
        if output != 'theory':
            cmd = np.genfromtxt(f.read(basename + '.cmd').decode().split('\n'),
                                skip_header=14, names=True, dtype=None)
            cmd = rfn.drop_fields(cmd, track.dtype.names[1:])
            track = rfn.join_by('star_age', track, cmd, jointype='inner', usemask=False)

        tracks.append(track)

    return tracks


def get_isochrone(t=1.0, **kwargs):
    """Returns a single isochrone from the MIST database with
    age ``t`` (in Gyr) and metallicity [Fe/H] ``FeH``.  The
    script makes the PHP request, infers the filename,
    and returns a NumPy structured array.  You can
    get the list of column names with e.g.

        isochrone = mistery.get_isochrone(t=0.3, FeH=-0.25)
        print(isochrone.dtype.names)

    """
    return get_isochrones(ts=[t], split=False, **kwargs)


def get_isochrones(ts=[1.0], split=True, FeH=0.0, vvcrit=0.0, Av=0.0, theory='basic',
                   photometry=None):
    """Returns a set of isochrones from the MIST database with
    ages ``ts`` (in Gyr) and metallicity [Fe/H] ``FeH``.  The
    script makes the PHP request, infers the filename,
    and returns a NumPy structured array.  You can
    get the list of column names with e.g.

        isochrones = mistery.get_isochrone(ts=[0.3, 1.3], FeH=-0.25)
        print(isochrones[0].dtype.names)

    The data is returned in a single ``.iso`` file, which is split up
    into a list of arrays for each age if ``split=True``.  Otherwise,
    a single array is returned that contains all the isochrones.
    """
    # choosing an age more precisely than 10ppm causes a variety of issues
    if any([np.abs(t-np.round(t, 5-int(np.log10(t)))) > 2*np.finfo(type(t)).resolution for t in ts]):
        raise ValueError

    data={
        'version': '1.2',
        'v_div_vcrit': 'vvcrit%.1f' % vvcrit,
        'age_scale': 'linear',
        'age_type': 'list',
        'age_value': '',
        'age_list': ' '.join(['%g' % (t*1e9) for t in ts]),
        'FeH_value': '%g' % FeH,
        'Av_value': '%g' % Av
    }

    # fetch theory, if requested
    if theory in {'basic', 'full'}:
        data['output_option'] = 'theory'
        data['theory_output'] = theory

        r = requests.post(
            BASE_URL+'iso_form.php',
            data=data
        )

        filename = r.text[18:48]
        f = io.BytesIO(urlopen(BASE_URL + filename).read()) # not a zip file
        isos = np.genfromtxt(f, skip_header=10, names=True, dtype=None)
    elif theory is not None:
        raise ValueError

    # fetch photometry, if requested
    if photometry is not None:
        data['output_option'] = 'photometry'
        data['output'] = photometry

        r = requests.post(
            BASE_URL+'iso_form.php',
            data=data
        )
        filename = r.text[18:52]

        f = ZipFile(io.BytesIO(urlopen(BASE_URL + filename).read()))

        cmds = np.genfromtxt(f.read(f.namelist()[0]).decode().split('\n'),
                             skip_header=12, names=True, dtype=None)

        if theory is None:
            # no theory data, so photometry is everything
            isos = cmd
        else:
            # combine theory and photometry
            cmds = rfn.drop_fields(cmds, isos.dtype.names)
            isos = rfn.append_fields(isos, cmds.dtype.names, [cmds[k] for k in cmds.dtype.names], usemask=False)

    if not split:
        return isos
    else:
        return [isos[np.isclose(isos['isochrone_age_yr']/1e9, t)] for t in ts]
