import os
from collections import OrderedDict
from datetime import datetime
from math import ceil, floor

import cdsapi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import xarray as xr
from matplotlib import ticker
from matplotlib.colors import Normalize
from netCDF4 import Dataset
from numba import float64
from numba.experimental import jitclass
from numba.types import unicode_type

from ..queryreport import print_text
from ..utilities.utilities import (
    SA_Density_array,
    SA_Density_value,
    SA_Pressure_array,
    SA_Pressure_value,
    SA_Temperature_array,
    SA_Temperature_value,
    interp_ex_array,
    interp_ex_value,
)

MetData_spec = OrderedDict()
MetData_spec["z_data"] = float64[::1]
MetData_spec["temperature_data"] = float64[::1]
MetData_spec["pressure_data"] = float64[::1]
MetData_spec["density_data"] = float64[::1]
MetData_spec["wind_U_data"] = float64[::1]
MetData_spec["wind_V_data"] = float64[::1]
MetData_spec["source"] = unicode_type
MetData_spec["surface_temperature"] = float64  # surface temperature
MetData_spec["surface_pressure"] = float64  # surface pressure
MetData_spec["lapse_tropos"] = float64  # lapse rate in troposphere
MetData_spec["lapse_stratos"] = float64  # lapse rate stratosphere
MetData_spec["height_tropos"] = float64  # height of the troposphere
MetData_spec["height_stratos"] = float64  # height of the stratosphere
MetData_spec["Ra"] = float64  # gas constant of dry air
MetData_spec["g"] = float64  # gravitational acceleration


@jitclass(MetData_spec)
class MetData:
    def __init__(
        self,
        source="standardAtmos",
        surface_temperature=293,
        surface_pressure=101325,
        lapse_tropos=6.5e-3,
        lapse_stratos=2.0e-3,
        height_tropos=11e3,
        height_stratos=20e3,
        Ra=285,
        g=9.81,
    ):
        self.surface_temperature = np.float64(surface_temperature)
        self.surface_pressure = np.float64(surface_pressure)
        self.lapse_tropos = np.float64(lapse_tropos)
        self.lapse_stratos = np.float64(lapse_stratos)
        self.height_tropos = np.float64(height_tropos)
        self.height_stratos = np.float64(height_stratos)
        self.Ra = np.float64(Ra)
        self.g = np.float64(g)
        self.source = source

        self.z_data = np.empty((0), dtype=np.float64)
        self.temperature_data = np.empty((0), dtype=np.float64)
        self.pressure_data = np.empty((0), dtype=np.float64)
        self.density_data = np.empty((0), dtype=np.float64)
        self.wind_U_data = np.empty((0), dtype=np.float64)
        self.wind_V_data = np.empty((0), dtype=np.float64)

    def set_zuv_data(self, z, u, v):
        self.z_data = z
        self.wind_U_data = u
        self.wind_V_data = v

    def temperature_array(self, z):
        if self.source in ["netCDF", "GFS", "GFS Archive"]:
            temperature = interp_ex_array(z, self.z_data, self.temperature_data)
        if self.source == "standardAtmos":
            temperature = SA_Temperature_array(
                z,
                self.surface_temperature,
                self.lapse_tropos,
                self.lapse_stratos,
                self.height_tropos,
                self.height_stratos,
            )
        return temperature

    def temperature_value(self, z):
        if self.source in ["netCDF", "GFS", "GFS Archive"]:
            temperature = interp_ex_value(z, self.z_data, self.temperature_data)
        if self.source == "standardAtmos":
            temperature = SA_Temperature_value(
                z,
                self.surface_temperature,
                self.lapse_tropos,
                self.lapse_stratos,
                self.height_tropos,
                self.height_stratos,
            )
        return temperature

    def pressure_array(self, z):
        if self.source in ["netCDF", "GFS", "GFS Archive"]:
            pressure = interp_ex_array(z, self.z_data, self.pressure_data)
        elif self.source == "standardAtmos":
            pressure = SA_Pressure_array(
                z,
                self.surface_temperature,
                self.surface_pressure,
                self.lapse_tropos,
                self.lapse_stratos,
                self.height_tropos,
                self.height_stratos,
                self.g,
                self.Ra,
            )
        return pressure

    def pressure_value(self, z):
        if self.source in ["netCDF", "GFS", "GFS Archive"]:
            pressure = interp_ex_value(z, self.z_data, self.pressure_data)
        elif self.source == "standardAtmos":
            pressure = SA_Pressure_value(
                z,
                self.surface_temperature,
                self.surface_pressure,
                self.lapse_tropos,
                self.lapse_stratos,
                self.height_tropos,
                self.height_stratos,
                self.g,
                self.Ra,
            )
        return pressure

    def density_array(self, z):
        if self.source in ["netCDF", "GFS", "GFS Archive"]:
            density = interp_ex_array(z, self.z_data, self.density_data)
        elif self.source == "standardAtmos":
            density = SA_Density_array(
                z,
                self.surface_temperature,
                self.surface_pressure,
                self.lapse_tropos,
                self.lapse_stratos,
                self.height_tropos,
                self.height_stratos,
                self.g,
                self.Ra,
            )
        return density

    def density_value(self, z):
        if self.source in ["netCDF", "GFS", "GFS Archive"]:
            density = interp_ex_value(z, self.z_data, self.density_data)
        elif self.source == "standardAtmos":
            density = SA_Density_value(
                z,
                self.surface_temperature,
                self.surface_pressure,
                self.lapse_tropos,
                self.lapse_stratos,
                self.height_tropos,
                self.height_stratos,
                self.g,
                self.Ra,
            )
        return density

    def wind_U_array(self, z, scale=None):
        u = interp_ex_array(z, self.z_data, self.wind_U_data)
        if scale is None:
            ret = u
        else:
            ret = u / scale
        return ret

    def wind_U_value(self, z, scale=None):
        u = interp_ex_value(z, self.z_data, self.wind_U_data)
        if scale is None:
            ret = u
        else:
            ret = u / scale
        return ret

    def wind_V_array(self, z, scale=None):
        v = interp_ex_array(z, self.z_data, self.wind_V_data)
        if scale is None:
            ret = v
        else:
            ret = v / scale
        return ret

    def wind_V_value(self, z, scale=None):
        v = interp_ex_value(z, self.z_data, self.wind_V_data)
        if scale is None:
            ret = v
        else:
            ret = v / scale
        return ret

    def wind_speed_array(self, z):
        u = self.wind_U_array(z)
        v = self.wind_V_array(z)
        spd = np.sqrt(u * u + v * v)
        return spd

    def wind_speed_value(self, z):
        u = self.wind_U_value(z)
        v = self.wind_V_value(z)
        spd = np.sqrt(u * u + v * v)
        return spd

    def max_wind_speed(self, H, num=100):
        z = np.arange(0.0, H + 1.0, H / (num - 1), dtype=np.float64)
        spd = self.wind_speed_array(z)
        return np.amax(spd)

    def settling_speed_array(self, params, z, scale=None):
        Ws = self.calculate_settling_speed_array(params, z)
        if scale is None:
            ret = Ws
        else:
            ret = Ws / scale
        return ret

    def settling_speed_value(self, params, z, scale=None):
        Ws = self.calculate_settling_speed_value(params, z)
        if scale is None:
            ret = Ws
        else:
            ret = Ws / scale
        return ret

    def settling_speed_for_grain_class_array(self, params, grain_i, z, scale=None):
        Ws = self.calculate_settling_speed_for_grain_class_array(params, grain_i, z)
        if scale is None:
            ret = Ws
        else:
            ret = Ws / scale
        return ret

    def settling_speed_for_grain_class_value(self, params, grain_i, z, scale=None):
        Ws = self.calculate_settling_speed_for_grain_class_value(params, grain_i, z)
        if scale is None:
            ret = Ws
        else:
            ret = Ws / scale
        return ret

    @staticmethod
    def _solve_settling_function(diam, g, rho_p, rho_a, mu, max_iter=50):

        tolerance = 1e-12

        x0 = np.float64(1e-6)
        x1 = np.float64(10000)

        def _settling_func_white(Re, d, g, rho_p, rho_a, mu):
            gp = (rho_p - rho_a) * g / rho_a
            C1 = 0.25
            C2 = 6.0
            Cd = C1 + 24.0 / Re + C2 / (1 + np.sqrt(Re))
            d3 = d**3
            f = Cd * Re * Re - 4.0 / 3.0 * gp * d3 * (rho_a / mu) ** 2
            return f

        fx0 = _settling_func_white(x0, diam, g, rho_p, rho_a, mu)
        fx1 = _settling_func_white(x1, diam, g, rho_p, rho_a, mu)

        if np.abs(fx0) < np.abs(fx1):
            x0, x1 = x1, x0
            fx0, fx1 = fx1, fx0

        x2, fx2 = x0, fx0
        d = x2

        mflag = np.bool(True)
        steps_taken = 0

        while steps_taken < max_iter and np.abs(x1 - x0) > tolerance:
            fx0 = _settling_func_white(x0, diam, g, rho_p, rho_a, mu)
            fx1 = _settling_func_white(x1, diam, g, rho_p, rho_a, mu)
            fx2 = _settling_func_white(x2, diam, g, rho_p, rho_a, mu)

            if fx0 != fx2 and fx1 != fx2:
                L0 = (x0 * fx1 * fx2) / ((fx0 - fx1) * (fx0 - fx2))
                L1 = (x1 * fx0 * fx2) / ((fx1 - fx0) * (fx1 - fx2))
                L2 = (x2 * fx1 * fx0) / ((fx2 - fx0) * (fx2 - fx1))
                new = L0 + L1 + L2
            else:
                new = x1 - fx1 * (x1 - x0) / (fx1 - fx0)

            if (
                (new < 0.25 * (3 * x0 + x1) or new > x1)
                or (mflag and np.abs(new - x1) >= 0.5 * np.abs(x1 - x2))
                or ((not mflag) and np.abs(new - x1) >= 0.5 * np.abs(x2 - d))
                or (mflag and np.abs(x1 - x2) < tolerance)
                or ((not mflag) and np.abs(x2 - d) < tolerance)
            ):
                new = 0.5 * (x0 + x1)
                mflag = np.bool(True)
            else:
                mflag = np.bool(False)

            fnew = _settling_func_white(new, diam, g, rho_p, rho_a, mu)
            d, x2 = x2, x1

            if fx0 * fnew < 0:
                x1 = new
            else:
                x0 = new

            if np.abs(fx0) < np.abs(fx1):
                x0, x1 = x1, x0

            steps_taken += 1

        return x1, steps_taken

    def calculate_settling_speed_array(self, params, z):

        ws = np.empty((z.size, params.grains.bins), dtype=np.float64)

        rho_a = np.empty((z.size, 1), dtype=np.float64)
        rho_a = self.density_array(z)

        for iz, rho_az in enumerate(rho_a):

            for j, (d, rho_p) in enumerate(
                zip(params.grains.diameter, params.grains.density)
            ):

                Re, steps_taken = self._solve_settling_function(
                    d, params.physical.g, rho_p, rho_az, params.physical.mu
                )
                if steps_taken > 50:
                    raise RuntimeError(
                        "In MetData: _solve_settling_function" + " failed to converge"
                    )
                ws[iz, j] = params.physical.mu * Re / rho_az / d

        return ws

    def calculate_settling_speed_value(self, params, z):

        ws = np.empty((params.grains.bins), dtype=np.float64)

        rho_a = self.density_value(z)

        for j, (d, rho_p) in enumerate(
            zip(params.grains.diameter, params.grains.density)
        ):

            Re, steps_taken = self._solve_settling_function(
                d, params.physical.g, rho_p, rho_a, params.physical.mu
            )
            if steps_taken > 50:
                raise RuntimeError(
                    "In MetData: _solve_settling_function" + " failed to converge"
                )
            ws[j] = params.physical.mu * Re / rho_a / d

        return ws

    def calculate_settling_speed_for_grain_class_array(self, params, grain_i, z):

        ws = np.empty((z.size, 1), dtype=np.float64)

        rho_a = np.empty((z.size, 1), dtype=np.float64)
        rho_a = self.density_array(z)

        for iz, rho_az in enumerate(rho_a):

            d = params.grains.diameter[grain_i]
            rho_p = params.grains.density[grain_i]

            Re, steps_taken = self._solve_settling_function(
                d, params.physical.g, rho_p, rho_az, params.physical.mu
            )
            if steps_taken > 50:
                raise RuntimeError(
                    "In MetData: _solve_settling_function" + " failed to converge"
                )
            ws[iz, 1] = params.physical.mu * Re / rho_az / d

        return ws

    def calculate_settling_speed_for_grain_class_value(self, params, grain_i, z):

        rho_a = self.density_value(z)

        d = params.grains.diameter[grain_i]
        rho_p = params.grains.density[grain_i]

        Re, steps_taken = self._solve_settling_function(
            d, params.physical.g, rho_p, rho_a, params.physical.mu
        )
        if steps_taken > 50:
            raise RuntimeError(
                "In MetData: _solve_settling_function" + " failed to converge"
            )
        ws = params.physical.mu * Re / rho_a / d

        return ws


# pylint: disable=E1101
MetData_type = MetData.class_type.instance_type


def save_met(met, file="meteorology.npz"):
    if os.path.exists(file):
        print(
            "WARNING: {outname} ".format(outname=file)
            + "already exists and will be replaced"
        )

    if met.source == "standardAtmos":
        np.savez(
            file,
            source=met.source,
            surface_temperature=met.surface_temperature,
            surface_pressure=met.surface_pressure,
            lapse_tropos=met.lapse_tropos,
            lapse_stratos=met.lapse_stratos,
            height_tropos=met.height_tropos,
            height_stratos=met.height_stratos,
            Ra=met.Ra,
            g=met.g,
            z_data=met.z_data,
            wind_U_data=met.wind_U_data,
            wind_V_data=met.wind_V_data,
        )
    elif met.source in ["netCDF", "GFS"]:
        np.savez(
            file,
            source=met.source,
            Ra=met.Ra,
            g=met.g,
            z_data=met.z_data,
            wind_U_data=met.wind_U_data,
            wind_V_data=met.wind_V_data,
            temperature_data=met.temperature_data,
            pressure_data=met.pressure_data,
            density_data=met.density_data,
        )


def load_met(met_file):

    if not os.path.exists(met_file):
        raise IOError("AshDisperse meteorological file {} not found".format(met_file))

    met = MetData()
    data = np.load(met_file)

    if str(data["source"]) == "standardAtmos":
        met = MetData(
            source="standardAtmos",
            surface_temperature=np.float64(data["surface_temperature"]),
            surface_pressure=np.float64(data["surface_pressure"]),
            lapse_tropos=np.float64(data["lapse_tropos"]),
            lapse_stratos=np.float64(data["lapse_stratos"]),
            height_tropos=np.float64(data["height_tropos"]),
            height_stratos=np.float64(data["height_stratos"]),
            Ra=np.float64(data["Ra"]),
            g=np.float64(data["g"]),
        )
        met.set_zuv_data(data["Z"], data["U"], data["V"])
    elif str(data["source"]) in ["netCDF", "GFS"]:
        met = MetData(
            source="netCDF", Ra=np.float64(data["Ra"]), g=np.float64(data["g"])
        )
        met.z_data = data["z_data"]
        met.wind_U_data = data["wind_U_data"]
        met.wind_V_data = data["wind_V_data"]
        met.temperature_data = data["temperature_data"]
        met.pressure_data = data["pressure_data"]
        met.density_data = data["density_data"]

    return met


def netCDF_to_Met(met, netcdf_data):
    N = len(netcdf_data.altitude)
    met.z_data = np.empty((N), dtype=np.float64)
    met.z_data[:N] = netcdf_data.altitude[:N]
    met.wind_U_data = np.empty((N), dtype=np.float64)
    met.wind_U_data[:N] = netcdf_data.wind_U[:N]
    met.wind_V_data = np.empty((N), dtype=np.float64)
    met.wind_V_data[:N] = netcdf_data.wind_V[:N]
    met.temperature_data = np.empty((N), dtype=np.float64)
    met.temperature_data[:N] = netcdf_data.temperature[:N]
    met.pressure_data = np.empty((N), dtype=np.float64)
    met.pressure_data[:N] = netcdf_data.pressure[:N]
    met.density_data = np.empty((N), dtype=np.float64)
    met.density_data[:N] = netcdf_data.density[:N]
    met.source = "netCDF"
    return met


def gfs_to_Met(met, gfs_data, Ra=287.058):
    z = gfs_data.variables["Geopotential_height_isobaric"]
    temp = gfs_data.variables["Temperature_isobaric"]
    u = gfs_data.variables["u-component_of_wind_isobaric"]
    v = gfs_data.variables["v-component_of_wind_isobaric"]
    pres_name = temp.coordinates.split()[-1]
    pres = gfs_data.variables[pres_name]

    N = gfs_data.variables[pres_name].size

    met.z_data = np.empty((N), dtype=np.float64)
    met.z_data[:N] = np.flipud(z[:].data.flatten())

    met.wind_U_data = np.empty((N), dtype=np.float64)
    met.wind_U_data[:N] = np.flipud(u[:].data.flatten())

    met.wind_V_data = np.empty((N), dtype=np.float64)
    met.wind_V_data[:N] = np.flipud(v[:].data.flatten())

    met.temperature_data = np.empty((N), dtype=np.float64)
    met.temperature_data[:N] = np.flipud(temp[:].data.flatten())

    met.pressure_data = np.empty((N), dtype=np.float64)
    met.pressure_data[:N] = np.flipud(pres[:].data.flatten())

    met.density_data = np.empty((N), dtype=np.float64)
    met.density_data[:N] = met.pressure_data[:N] / Ra / met.temperature_data[:N]

    met.source = "GFS"
    return met


class netCDF:
    def __init__(self, file, lat, lon, Ra=287.058, g=9.80665):
        self.file = file
        self.lat = lat
        self.lon = lon
        self.Ra = Ra
        self.g = g

        self.altitude = np.empty((0), dtype=np.float64)
        self.wind_U = np.empty((0), dtype=np.float64)
        self.wind_V = np.empty((0), dtype=np.float64)
        self.temperature = np.empty((0), dtype=np.float64)
        self.pressure = np.empty((0), dtype=np.float64)
        self.density = np.empty((0), dtype=np.float64)

    def extract(self):
        nc = Dataset(self.file, "r")
        P = nc.variables["level"][:] * 100

        lats = nc.variables["latitude"][:].data
        lons = nc.variables["longitude"][:].data

        if np.amax(lons) > 180.0:
            lons[lons > 180.0] = 180.0 - lons[lons > 180.0]

        lat_i0, _, lon_i0, _ = _near_lat_lon(self.lat, self.lon, lats, lons)

        Z = nc.variables["z"][0, :, lat_i0, lon_i0] / self.g
        self.altitude = np.float64(np.asarray(np.flipud(Z)))

        Uij = _interp_latlon(self.lat, self.lon, nc.variables["u"], lats, lons)
        Vij = _interp_latlon(self.lat, self.lon, nc.variables["v"], lats, lons)
        Tij = _interp_latlon(self.lat, self.lon, nc.variables["t"], lats, lons)

        self.wind_U = np.float64(np.asarray(np.flipud(Uij)))
        self.wind_V = np.float64(np.asarray(np.flipud(Vij)))
        self.temperature = np.float64(np.asarray(np.flipud(Tij)))

        self.pressure = np.float64(np.asarray(np.flipud(P)))
        self.density = np.float64(np.asarray(np.flipud(P / self.Ra / Tij)))

    def download(self, *, datetime):
        if os.path.isfile(self.file):
            print_text("Met file {} exists and will be overwritten".format(self.file))

        cds = cdsapi.Client()
        cds.retrieve(
            "reanalysis-era5-pressure-levels",
            {
                "product_type": "reanalysis",
                "format": "netcdf",
                "variable": [
                    "geopotential",
                    "temperature",
                    "u_component_of_wind",
                    "v_component_of_wind",
                ],
                "pressure_level": [
                    "1",
                    "2",
                    "3",
                    "5",
                    "7",
                    "10",
                    "20",
                    "30",
                    "50",
                    "70",
                    "100",
                    "125",
                    "150",
                    "175",
                    "200",
                    "225",
                    "250",
                    "300",
                    "350",
                    "400",
                    "450",
                    "500",
                    "550",
                    "600",
                    "650",
                    "700",
                    "750",
                    "775",
                    "800",
                    "825",
                    "850",
                    "875",
                    "900",
                    "925",
                    "950",
                    "975",
                    "1000",
                ],
                "year": str(datetime.year),
                "month": "{:02d}".format(datetime.month),
                "day": "{:02d}".format(datetime.day),
                "time": "{:02d}:00".format(datetime.hour),
                "area": [
                    ceil(self.lat + 0.25),
                    floor(self.lon - 0.25),
                    floor(self.lat - 0.25),
                    ceil(self.lon + 0.25),
                ],
            },
            self.file,
        )


class gfs_archive:
    def __init__(self, cycle_datetime, forecast_hr, lat, lon, Ra=287.058, g=9.80665):

        self.lat = lat
        self.lon = lon % 360
        self.Ra = Ra
        self.g = g

        self.forecast_hr = forecast_hr
        self.cycle_datetime = pd.to_datetime(cycle_datetime)

        self.url = self._aws_site()
        self.idx_url = self.url + ".idx"

        grib_exists = self._check_grib()
        idx_exists = self._check_idx()

        if grib_exists and idx_exists:
            self.idx = self._get_idx_as_dataframe()

            self.levels = self.idx.loc[
                (self.idx["level"].str.match("(\d+(?:\.\d+)?) mb"))
            ].level.unique()

    def _aws_site(self):
        return f"https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.{self.cycle_datetime:%Y%m%d/%H}/atmos/gfs.t{self.cycle_datetime:%H}z.pgrb2.0p25.f{self.forecast_hr:03d}"

    def _check_grib(self):
        head = requests.head(self.url)
        check_exists = head.ok
        if check_exists:
            check_content = int(head.raw.info()["Content-Length"]) > 1_000_000
            return check_exists and check_content
        else:
            return False

    def _check_idx(self):
        idx_exists = requests.head(self.idx_url).ok
        return idx_exists

    def _get_idx_as_dataframe(self):
        df = pd.read_csv(
            self.idx_url,
            sep=":",
            names=[
                "grib_message",
                "start_byte",
                "reference_time",
                "variable",
                "level",
                "forecast_time",
                "?",
                "??",
                "???",
            ],
        )

        # Format the DataFrame
        df["reference_time"] = pd.to_datetime(df.reference_time, format="d=%Y%m%d%H")
        df["valid_time"] = df["reference_time"] + pd.to_timedelta(
            f"{self.forecast_hr}H"
        )
        df["start_byte"] = df["start_byte"].astype(int)
        df["end_byte"] = df["start_byte"].shift(-1, fill_value="")
        # TODO: Check this works: Assign the ending byte for the last row...
        # TODO: df["end_byte"] = df["start_byte"].shift(-1, fill_value=requests.get(self.grib, stream=True).headers['Content-Length'])
        # TODO: Based on what Karl Schnieder did.
        df["range"] = df.start_byte.astype(str) + "-" + df.end_byte.astype(str)
        df = df.reindex(
            columns=[
                "grib_message",
                "start_byte",
                "end_byte",
                "range",
                "reference_time",
                "valid_time",
                "variable",
                "level",
                "forecast_time",
                "?",
                "??",
                "???",
            ]
        )

        df = df.dropna(how="all", axis=1)
        df = df.fillna("")

        df["search_this"] = (
            df.loc[:, "variable":]
            .astype(str)
            .apply(
                lambda x: ":" + ":".join(x).rstrip(":").replace(":nan:", ":"),
                axis=1,
            )
        )

        # # Attach some attributes
        # df.attrs = dict(
        #     url=self.idx_url,
        #     description="Inventory index file for the GRIB2 file.",
        #     lead_time=self.forecast_hr,
        #     datetime=self.cycle_datetime,
        # )

        return df

    def read_idx(self, searchString=None):
        """
        Inspect the GRIB2 file contents by reading the index file.

        This reads index files created with the wgrib2 utility.

        Parameters
        ----------
        searchString : str
            Filter dataframe by a searchString regular expression.
            Searches for strings in the index file lines, specifically
            the variable, level, and forecast_time columns.
            Execute ``_searchString_help()`` for examples of a good
            searchString.

            .. include:: ../../user_guide/searchString.rst

        Returns
        -------
        A Pandas DataFrame of the index file.
        """

        # Filter DataFrame by searchString
        if searchString not in [None, ":"]:
            logic = self.idx.search_this.str.contains(searchString)
            if logic.sum() == 0:
                print(
                    f"No GRIB messages found. There might be something wrong with {searchString=}"
                )
            df = self.idx.loc[logic]
        return df

    def download_grib(self, searchString, outFile="./gfs_grib_file.grib2"):

        grib_source = self.url

        # Download subsets of the file by byte range with cURL.
        # > Instead of using a single curl command for each row,
        # > group adjacent messages in the same curl command.

        # Find index groupings
        # TODO: Improve this for readability
        # https://stackoverflow.com/a/32199363/2383070
        idx_df = self.read_idx(searchString)
        li = idx_df.index
        inds = (
            [0]
            + [ind for ind, (i, j) in enumerate(zip(li, li[1:]), 1) if j - i > 1]
            + [len(li) + 1]
        )

        curl_groups = [li[i:j] for i, j in zip(inds, inds[1:])]
        curl_ranges = []
        group_dfs = []
        for i, group in enumerate(curl_groups):
            _df = idx_df.loc[group]
            curl_ranges.append(f"{_df.iloc[0].start_byte}-{_df.iloc[-1].end_byte}")
            group_dfs.append(_df)

            for i, (range, _df) in enumerate(zip(curl_ranges, group_dfs)):

                if i == 0:
                    # If we are working on the first item, overwrite the existing file...
                    curl = f"curl -s --range {range} {grib_source} > {outFile}"
                else:
                    # ...all other messages are appended to the subset file.
                    curl = f"curl -s --range {range} {grib_source} >> {outFile}"
                os.system(curl)

    def profiles(self):

        data_P = np.zeros(self.levels.size)
        data_Z = np.zeros(self.levels.size)
        data_T = np.zeros(self.levels.size)
        data_U = np.zeros(self.levels.size)
        data_V = np.zeros(self.levels.size)

        outFile = "./gfs_grib_file.grib2"

        for j, l in enumerate(self.levels):
            data_P[j] = np.float64(l.replace(" mb", "")) * 100

            self.download_grib(f":HGT:{l}", outFile=outFile)

            Z = xr.load_dataset(outFile, engine="cfgrib")
            data_Z[j] = np.float64(
                Z["gh"]
                .interp(latitude=self.lat, longitude=self.lon, method="cubic")
                .values
            )
            self.download_grib(f":TMP:{l}", outFile="./gfs_grib_file.grib2")
            T = xr.load_dataset(outFile, engine="cfgrib")
            data_T[j] = np.float64(
                T["t"]
                .interp(latitude=self.lat, longitude=self.lon, method="cubic")
                .values
            )
            self.download_grib(f":(?:U|V)GRD:{l}", outFile="./gfs_grib_file.grib2")
            UV = xr.load_dataset(outFile, engine="cfgrib")
            uv_interp = UV.interp(latitude=self.lat, longitude=self.lon, method="cubic")
            data_U[j] = np.float64(uv_interp["u"].values)
            data_V[j] = np.float64(uv_interp["v"].values)

        df = pd.DataFrame(
            columns=["altitude", "temperature", "pressure", "wind_U", "wind_V"]
        )
        df["altitude"] = data_Z
        df["temperature"] = data_T
        df["pressure"] = data_P
        df["wind_U"] = data_U
        df["wind_V"] = data_V

        df = df.dropna()
        df = df.sort_values("altitude", ignore_index=True)

        return df


def gfs_archive_to_Met(met, gfs_data, Ra=287.058):
    z = gfs_data.altitude.values
    temp = gfs_data.temperature.values
    u = gfs_data.wind_U.values
    v = gfs_data.wind_V.values
    pres = gfs_data.pressure.values

    N = gfs_data.pressure.size

    met.z_data = np.empty((N), dtype=np.float64)
    met.z_data[:N] = z[:]

    met.wind_U_data = np.empty((N), dtype=np.float64)
    met.wind_U_data[:N] = u[:]

    met.wind_V_data = np.empty((N), dtype=np.float64)
    met.wind_V_data[:N] = v[:]

    met.temperature_data = np.empty((N), dtype=np.float64)
    met.temperature_data[:N] = temp[:]

    met.pressure_data = np.empty((N), dtype=np.float64)
    met.pressure_data[:N] = pres[:]

    met.density_data = np.empty((N), dtype=np.float64)
    met.density_data[:N] = met.pressure_data[:N] / Ra / met.temperature_data[:N]

    met.source = "GFS Archive"
    return met


def _near_lat_lon(target_lat, target_lon, lats, lons):

    lat_i_near = np.abs(lats - target_lat).argmin()
    lon_i_near = np.abs(lons - target_lon).argmin()

    if target_lat in lats:
        lat_i0 = lat_i_near
        lat_i1 = lat_i_near  # won't need this
    else:
        lat_i0 = lat_i_near if lat_i_near < target_lat else lat_i_near + 1
        lat_i1 = lat_i0 - 1
    if target_lon in lons:
        lon_i0 = lon_i_near
        lon_i1 = lon_i_near  # won't need this
    else:
        lon_i0 = lon_i_near if lon_i_near < target_lon else lon_i_near - 1
        lon_i1 = lon_i0 + 1

    return lat_i0, lat_i1, lon_i0, lon_i1


def _interp_latlon(target_lat, target_lon, data, lats, lons):

    lat_i0, lat_i1, lon_i0, lon_i1 = _near_lat_lon(target_lat, target_lon, lats, lons)

    d_lat = target_lat - lats[lat_i0]
    d_lon = target_lon - lons[lon_i0]

    data_00 = data[0, :, lat_i0, lon_i0]
    data_01 = data[0, :, lat_i1, lon_i0]
    data_10 = data[0, :, lat_i0, lon_i1]
    data_11 = data[0, :, lat_i1, lon_i1]

    data_i0 = data_00 + d_lon * (data_10 - data_00)
    data_i1 = data_01 + d_lon * (data_11 - data_01)
    data_ij = data_i0 + d_lat * (data_i1 - data_i0)

    return data_ij


def wind_scale(max_speed):

    max_log10 = np.log10(max_speed)
    major = []
    minor = []
    for j in range(np.int(max_log10) + 1):
        major.append(10**j)
        for k in range(2, 10):
            if k * 10**j > max_speed:
                break
            minor.append(k * 10**j)

    return major, minor


def wind_plot(met, z, show=True, savename=None):

    fig, ax = plt.subplots()

    U = met.wind_U_array(z)
    V = met.wind_V(z)
    speed = met.wind_speed(z)

    max_speed = speed.max()
    major, minor = wind_scale(max_speed)
    major.append(minor[-1])
    minor.pop(-1)

    ax.set_xlim(-max_speed, max_speed)
    ax.set_ylim(-max_speed, max_speed)
    ax.set_aspect("equal")
    ax.axis("off")

    cmap = plt.cm.viridis
    norm = Normalize(vmin=0, vmax=z[-1])
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=Normalize(vmin=0, vmax=z[-1]))

    ax.quiver(
        0,
        -max_speed,
        0,
        2 * max_speed,
        color="darkgray",
        headwidth=6,
        headlength=10,
        scale=1,
        scale_units="xy",
        angles="xy",
    )
    ax.quiver(
        -max_speed / 2,
        0,
        max_speed,
        0,
        color="darkgray",
        headwidth=1,
        headlength=0,
        scale=1,
        scale_units="xy",
        angles="xy",
    )
    ax.text(0, 1.1 * max_speed, "N")

    for m in major:
        ax.add_artist(plt.Circle((0, 0), m, ec="darkgray", lw=0.5, fill=False))
        ax.text(m * np.cos(45 * np.pi / 180), m * np.sin(45 * np.pi / 180), str(m))
    for m in minor:
        ax.add_artist(plt.Circle((0, 0), m, ec="darkgray", lw=0.25, fill=False))

    for (this_z, this_u, this_v) in zip(z, U, V):
        ax.quiver(
            0,
            0,
            this_u,
            this_v,
            color=cmap(norm(this_z)),
            scale=1,
            scale_units="xy",
            angles="xy",
        )

    fmt = ticker.FuncFormatter(lambda z, pos: "{:g}".format(z * 1e-3))
    cbar = fig.colorbar(sm, format=fmt)
    cbar.ax.set_title("Altitude (km)")

    if savename is not None:
        plt.savefig(savename)

    if show:
        plt.show()
    else:
        plt.close()

    return
