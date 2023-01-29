import mmap
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, Optional

import numpy as np
import pandas as pd

from proscan_log_api.utils import get_files


@dataclass
class TcsLog:
    data: pd.DataFrame
    metadata: Optional[pd.DataFrame] = None


class SlowControlClient:
    def __init__(
        self, root_dir: str = "/mnt/TCSlogs/", folders: List[str] | str = []
    ) -> None:
        self.root_dir = root_dir
        self.folders = folders

    def _get_units(self, units_b: bytes) -> List[str]:
        units = []
        for u in re.split(rb"\s+", units_b):
            if u:
                _match = re.match(rb"\[(\S+)\]", u)
                if _match:
                    units.append(_match.groups()[0].decode("utf-8"))
        return units

    def metadata(
        self, metadata_section: Optional[bytes] = None, file_path: Optional[str] = None
    ) -> pd.DataFrame:
        header_re = re.compile(
            rb"(\#\s\-+\n)((\#\s\S+\s+\S+\s+[\w\d\-\_\+\s\)\(\.]+)+)#\s\n#\s[\w\s\:]+\n#\s\n#\s+((([\w\d\-\_\+\)\(\.]+)\s*)+)\n#((\s+\[[\w\-]+\])+)"
        )
        match = []
        units = []

        if metadata_section:
            match = header_re.findall(metadata_section)
        elif file_path:
            with open(file_path, mode="r", encoding="utf-8") as file_obj:
                with mmap.mmap(
                    file_obj.fileno(), length=0, access=mmap.ACCESS_READ
                ) as mmap_obj:
                    match = header_re.findall(mmap_obj)

        if match:
            units = self._get_units(match[0][6])
        header_str = match[0][1].decode("utf-8")
        rows = re.findall(
            r"#\s(?P<Titel>\S+)\s+(?P<Key>\S+)\s+(?P<Description>.+)(?>\r\n|\r|\n)",
            header_str,
        )
        df = pd.DataFrame(rows, columns=["titel", "key", "description"])

        if units:
            df["unit"] = units
            new_row = pd.DataFrame(
                {
                    "titel": "timestamp",
                    "key": "timestamp",
                    "description": "timestamp",
                    "unit": "iso_datetime",
                },
                index=[0],
            )
        else:
            new_row = pd.DataFrame(
                {
                    "titel": "timestamp",
                    "key": "timestamp",
                    "description": "timestamp",
                },
                index=[0],
            )
        df = pd.concat([new_row, df.loc[:]]).reset_index(drop=True)
        return df

    def parse_slow_control(
        self, file_path: str, metadata: bool = False
    ) -> Optional[TcsLog]:
        split = re.compile(rb"(?P<metadata>((#\s.*\n)+))(?P<body>([^#].*\n)+)")
        with open(file_path, mode="r", encoding="utf-8") as file_obj:
            with mmap.mmap(
                file_obj.fileno(), length=0, access=mmap.ACCESS_READ
            ) as mmap_obj:
                separated_log = split.match(mmap_obj)
                if separated_log:
                    groups = separated_log.groupdict()
                    metadata = self.metadata(metadata_section=groups["metadata"])
                    body = groups["body"].decode("utf-8")
                    data_list = [re.split(r"\s+", x) for x in body.split("\n")]
                    df = pd.DataFrame(data_list)
                    df[0] = df[0] + " " + df[1]
                    df.drop(columns=[1], inplace=True)
                    df.replace("", np.nan, inplace=True)
                    df.dropna(how="all", axis=1, inplace=True)
                    df.dropna(how="all", axis=0, inplace=True)
                    df.columns = metadata["titel"]
                    df.columns.name = ""
                    df["timestamp"] = pd.to_datetime(
                        df["timestamp"], format="%Y-%m-%d %H:%M:%S"
                    )
                    return TcsLog(data=df, metadata=metadata)
        return None

    def get(
        self,
        system: Literal["tvs", "tds"],
        folders: List[str] | str = [],
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
        area: Literal["G2", "G3", "O2"] | None = None,
    ) -> Optional[TcsLog]:
        log_list = []

        if not folders:
            if self.folders:
                folders = self.folders
            else:
                raise Exception("Please provide the folders to be searched!")

        for file in get_files(
            root_dir=self.root_dir,
            folders=folders,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            area=area,
            tcs_type="SlowControl",
            system=system,
        ):
            log = self.parse_slow_control(file)
            if log.data is not None:
                log_list.append(log)
        if log_list:
            if len(log_list) > 1:
                logs_data = pd.concat([log.data for log in log_list])
            else:
                logs_data = log.data
        logs_data.set_index("timestamp", inplace=True)
        logs_metadata = (
            pd.concat([log.metadata for log in log_list])
            .drop_duplicates("titel")
            .reset_index(drop=True)
        )
        logs_metadata = logs_metadata[~logs_metadata["titel"].isin(logs_data.columns)]
        if start_datetime and end_datetime:
            result_df = logs_data[
                (logs_data.index >= start_datetime) & (logs_data.index <= end_datetime)
            ]
        elif start_datetime and not end_datetime:
            result_df = (logs_data[logs_data.index >= start_datetime],)
        elif end_datetime and not start_datetime:
            result_df = (logs_data[logs_data.index <= end_datetime],)
        else:
            result_df = logs_data
        return TcsLog(data=result_df, metadata=logs_metadata)


class TcsTraceClient:
    def __init__(
        self, root_dir: str = "/mnt/TCSlogs/", folders: List[str] | str = []
    ) -> None:
        self.root_dir = root_dir
        self.folders = folders

    def parse_tcs_trace(self, file_path: str):
        df = pd.DataFrame()
        with open(file_path, mode="r", encoding="utf-8") as file_obj:
            with mmap.mmap(
                file_obj.fileno(), length=0, access=mmap.ACCESS_READ
            ) as mmap_obj:
                data_list = []
                lines = re.split(rb"\n", mmap_obj)
                for line in lines:
                    _match = re.match(
                        r"(?P<timestamp>\d{2}\.\d{2}\.\d{2}\s\d{2}\:\d{2}\:\d{2}.\d+)\s(?P<source>\w+)\s(?P<type>[^:]+):\s(?P<message>[^\n]+)",
                        line.decode("utf-8"),
                    )
                    if _match:
                        data_list.append(_match.groupdict())
                df = pd.DataFrame(data_list)
                df.replace("", np.nan, inplace=True)
                df.dropna(how="all", axis=1, inplace=True)
                df.dropna(how="all", axis=0, inplace=True)
                df["timestamp"] = pd.to_datetime(
                    df["timestamp"], format="%d.%m.%y %H:%M:%S.%f"
                )
        return df

    def get(
        self,
        system: Literal["tds", "tvs"],
        area: Optional[Literal["G2", "G3", "O2"]],
        folders: List[str] | str = [],
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        source: Optional[str] = None,
        signal_type: Optional[str] = None,
        message_regex: Optional[str] = None,
    ) -> Optional[TcsLog]:
        dataframes = []
        if not folders:
            if self.folders:
                folders = self.folders
            else:
                raise Exception("Please provide the folders to be searched!")

        for file in get_files(
            system=system,
            folders=folders,
            root_dir=self.root_dir,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            area=area,
            tcs_type="TcsTrace",
        ):
            dataframes.append(self.parse_tcs_trace(file))
        if dataframes:
            if len(dataframes) > 1:
                df = pd.concat(dataframes)
            else:
                df = dataframes[0]
        else:
            raise Exception("No data found!")
        df.set_index("timestamp", inplace=True)
        if start_datetime and end_datetime:
            result_df = df[(df.index >= start_datetime) & (df.index <= end_datetime)]
        elif start_datetime and not end_datetime:
            result_df = df[df.index >= start_datetime]
        elif end_datetime and not start_datetime:
            result_df = df[df.index <= end_datetime]
        else:
            result_df = df

        if source:
            result_df = result_df.loc[result_df["source"].values == source]
        if signal_type:
            result_df = result_df.loc[result_df["type"].values == signal_type]

        if message_regex:
            result_df = result_df[result_df["message"].str.contains(message_regex)]

        if isinstance(result_df, pd.DataFrame):
            result_df.reset_index(inplace=True)
            return TcsLog(data=result_df)
        else:
            return None
