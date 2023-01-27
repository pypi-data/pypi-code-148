"""
acquisitions includes functionality for analysing the timeline of
the SAR acquisitions.
"""

from dataclasses import dataclass

import numpy as np

import drama.geo as geosar
from drama.geo.geometry import inc_to_look

@dataclass
class PointTimeline:
    """PointTimeline keeps track of the variables that define the geometry of a
    point in the satellite track."""
    theta_i: np.ndarray
    northing: np.ndarray
    orbtime: np.ndarray
    orbnum: np.ndarray
    theta_l: np.ndarray
    slant_range: np.ndarray

class LatLonTimeline:
    """LatLonTimline holds data related to the acquisition timeline.

    Parameters
    ----------
    par_file : str | Path
        path to parameter file
    lats : float | np.ndarray
        input latitude coordinate [deg].
    lons : float | np.ndarray
        input longitude coordinate [deg].
    inc_angle_range : 2-elements list
        range of incident angles [deg].
    """

    def __init__(self, par_file, lats, lons, inc_angle_range, dlat=0.5, dlon=0.5):
        self.par_file = par_file
        self.lats = np.atleast_1d(lats)
        self.lons = np.atleast_1d(lons)
        self.inc_angle_range = inc_angle_range
        self.dlon = dlon
        self.dlat = dlat
        # make inc_angle_range wider by 1 degree
        inc_angle_range_wider = np.array((inc_angle_range)) + np.array((-1, 1))
        self.track = geosar.SingleSwath(
            par_file=self.par_file,
            inc_angle=inc_angle_range_wider,
        )

    def compute_timeline(self):
        """compute_timeline finds the ascensing and descending acquisitions over
        the region of interest.

        The region of interest is defined using the lats and lons with which the
        object is initalised. The swath is interpolated according to dlat and
        dlon.

        Returns
        -------
        tuple
            A tuple with two elements. The first is an array with the points
            along the ascending part of the orbits and the second with the
            descending.
        """
        self.track.interpolate_swath((self.dlat, self.dlon))
        ascending_acqs = self._compute_timeline(self.track.interpol.ascending)
        descending_acqs = self._compute_timeline(self.track.interpol.descending)
        return (ascending_acqs, descending_acqs)

    def _compute_timeline(self, interpolated_swath):
        """Iterates through all the orbits in a cycle and finds acquisitions
        within the region of interest.

        The initially the entries in the lon_indices array for orbits where the
        region of interest is not seen has NaNs. timeline_compress is called to
        remove these entries.

        Parameters
        ----------
        interpolated_swath : drama.geo.swath_geo.SingleTrack
            The swath for a single ascending or descending track.

        Returns
        -------
        np.ndarray
            Array filled with PointTimeline for each latitude and longitude.
        """
        mask_within_swath = np.logical_and(
            (interpolated_swath.inc_angle > np.deg2rad(self.inc_angle_range[0])),
            (interpolated_swath.inc_angle < np.deg2rad(self.inc_angle_range[1])),
        )
        lat_interpolated = interpolated_swath.lat
        lon_interpolated = interpolated_swath.lon
        # Unwrap the longitudes
        lon_interpolated = np.where(lon_interpolated > 0, lon_interpolated, lon_interpolated + 360)
        # The indices of the latitudes
        lat_indices = np.around((self.lats - lat_interpolated[0]) / self.dlat).astype(int)
        # Dimensions of output lon are n_orbis x lons
        n_orbits = int(self.track.norb)
        lon_dimensions = (n_orbits,) + self.lons.shape
        # Set all longitude indices to NaN.
        lon_indices = np.full(lon_dimensions, np.nan)
        # Torb is in hours
        lon_per_orbit = self.track.Torb * 360.0 / 24.0
        for i_orbit in range(n_orbits):
            lon_rotated = self.lons + lon_per_orbit * i_orbit
            lon_rotated = np.where(lon_rotated < 0, lon_rotated + 360, lon_rotated)
            lon_rotated = np.mod(lon_rotated, 360)
            current_lon = lon_rotated - lon_interpolated[0]
            current_lon = np.where(current_lon < 0, current_lon + 360, current_lon)
            this_ind = np.around(current_lon / self.dlon).astype(int)
            valid_indices = np.nonzero(
                (this_ind >= 0)
                & (this_ind < lon_interpolated.size)
                & (lat_indices >= 0)
                & (lat_indices < lat_interpolated.size)
            )
            if valid_indices[0].size > 0:
                val_cond_2 = mask_within_swath[lat_indices[valid_indices], this_ind[valid_indices]]
                valid_indices_ = (np.array([i_orbit] * valid_indices[0].size),) + valid_indices
                lon_indices[valid_indices_] = np.where(val_cond_2, this_ind[valid_indices], np.nan)
        acquisitions = timeline_compress(
            interpolated_swath,
            lat_indices,
            lon_indices,
            self.track.Horb,
        )
        return acquisitions


def timeline_compress(track, lat_ind_array, lon_ind_array, h_orb):
    """Compresses calculated timeline in order to turn vectors full on NAN
        values into lists.

        :author: Paco Lopez-Dekker

    Parameters
    ----------
    track : swath_geo.SingleTrack
        a Named tuple of the type SingleTrack, defined in swath_geo
    lat_ind_array : np.ndarray
        array of latitude indices
    lon_ind_array : np.ndarray
        array of longitude indices
    h_orb : float
        The height of the orbit [m].

    Returns
    -------
    np.ndarray
        Array filled with PointTimeline for each latitude and longitude.
    """

    # Dimensions of input, first dimension is orbit number
    dim_in = lon_ind_array.shape
    # Prepare output
    res = np.empty(dim_in[1:], dtype=object)
    if len(dim_in) == 2:
        # Transpose the data
        lon_ind_t = lon_ind_array.transpose()
        # Loop over one dimension
        for ind1 in range(dim_in[1]):
            # Look for regular values
            gd = np.nonzero(~np.isnan(lon_ind_t[ind1]))
            lat_ind = lat_ind_array[ind1].astype(int)
            lon_inds = lon_ind_t[ind1, gd].astype(int)
            theta_i = track.inc_angle[lat_ind, lon_inds.flatten()]
            northing = track.northing[lat_ind, lon_inds.flatten()]
            orbtime = track.time[lat_ind, lon_inds.flatten()]
            slant_range = track.slant_range[lat_ind, lon_inds.flatten()]
            theta_l = np.degrees(inc_to_look(theta_i, h_orb))

            res[ind1] = PointTimeline(
                theta_i, northing, orbtime, gd[0], theta_l, slant_range
            )

    elif len(dim_in) == 3:
        # Transpose the data
        lon_ind_t = lon_ind_array.transpose(1, 2, 0)
        # Loop over two dimension
        for ind1 in range(dim_in[1]):
            for ind2 in range(dim_in[2]):
                # Look for regular values
                gd = np.nonzero(~np.isnan(lon_ind_t[ind1, ind2]))
                lat_ind = lat_ind_array[ind1, ind2].astype(int)
                lon_inds = lon_ind_t[ind1, ind2, gd].astype(int)
                theta_i = track.inc_angle[lat_ind, lon_inds.flatten()]
                northing = track.northing[lat_ind, lon_inds.flatten()]
                orbtime = track.time[lat_ind, lon_inds.flatten()]
                theta_l = np.degrees(inc_to_look(theta_i, h_orb))
                slant_range = track.slant_range[lat_ind, lon_inds.flatten()]
                res[ind1, ind2] = PointTimeline(
                    theta_i, northing, orbtime, gd[0], theta_l, slant_range
                )
    else:
        raise ValueError("Too many dimensions in input parameter")
    return res
