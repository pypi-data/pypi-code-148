import os
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import xarray as xr


class gfs_archive:
    def __init__(self, run_datetime: str, fxx: int):

        self.fxx = fxx
        self.date = pd.to_datetime(run_datetime)

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
        return f"https://noaa-gfs-bdp-pds.s3.amazonaws.com/gfs.{self.date:%Y%m%d/%H}/atmos/gfs.t{self.date:%H}z.pgrb2.0p25.f{self.fxx:03d}"

    def _check_grib(self):
        head = requests.head(url)
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
        df["valid_time"] = df["reference_time"] + pd.to_timedelta(f"{self.fxx}H")
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

        # Attach some attributes
        df.attrs = dict(
            url=self.idx_url,
            description="Inventory index file for the GRIB2 file.",
            lead_time=self.fxx,
            datetime=self.date,
        )

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

    def profiles(self, latitude, longitude):

        data_P = np.zeros(levels.size)
        data_Z = np.zeros(levels.size)
        data_T = np.zeros(levels.size)
        data_U = np.zeros(levels.size)
        data_V = np.zeros(levels.size)

        outFile = "./gfs_grib_file.grib2"

        for j, l in enumerate(self.levels):
            data_P[j] = np.float64(l.replace(" mb", "")) * 100

            self.download_grib(f":HGT:{l}", outFile=outFile)

            Z = xr.load_dataset(outFile, engine="cfgrib")
            data_Z[j] = np.float64(
                Z["gh"]
                .interp(latitude=latitude, longitude=longitude, method="cubic")
                .values
            )
            self.download_grib(f":TMP:{l}", outFile="./gfs_grib_file.grib2")
            T = xr.load_dataset(outFile, engine="cfgrib")
            data_T[j] = np.float64(
                T["t"]
                .interp(latitude=latitude, longitude=longitude, method="cubic")
                .values
            )
            self.download_grib(f":(?:U|V)GRD:{l}", outFile="./gfs_grib_file.grib2")
            UV = xr.load_dataset(outFile, engine="cfgrib")
            uv_interp = UV.interp(
                latitude=latitude, longitude=longitude, method="cubic"
            )
            data_U[j] = np.float64(uv_interp["u"].values)
            data_V[j] = np.float64(uv_interp["v"].values)

        df = pd.DataFrame(columns=["Z", "T", "P", "U", "V"])
        df["Z"] = data_Z
        df["T"] = data_T
        df["P"] = data_P
        df["U"] = data_U
        df["V"] = data_V

        df = df.dropna()
        df = df.sort_values("Z", ignore_index=True)

        return df
