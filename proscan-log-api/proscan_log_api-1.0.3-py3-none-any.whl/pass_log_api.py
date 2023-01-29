import mmap
import re
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from concurrent.futures import as_completed
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import List, Literal, Optional
from itertools import repeat
import pandas as pd
import pytz

from proscan_log_api.utils import get_folders, get_pass_files

PASS_LOG_DAYS_QUERY_LIMIT = 30


@dataclass
class InterlockEventData:
    header: List[str]
    metadata: List[str]
    event: pd.DataFrame
    pre_events: Optional[pd.DataFrame]
    post_events: pd.DataFrame


def timestamp_to_int(timestamp: float) -> int:
    timestamp_str = str(timestamp).replace(".", "")
    timestamp = int(timestamp_str)
    return timestamp


def timestamp_to_datetime(timestamp: str) -> datetime:
    timestamp = timestamp.replace(".", "")
    if len(timestamp) > 10:
        timestamp = timestamp[:10] + "." + timestamp[10:]
    return datetime.fromtimestamp(float(timestamp), tz=pytz.timezone("Europe/Zurich"))


def timestamp_to_date_range(timestamp: str) -> List[date]:
    timestamp = timestamp.replace(".", "")
    if len(timestamp) > 10:
        timestamp = timestamp[:10] + "." + timestamp[10:]
        return [
            datetime.fromtimestamp(float(timestamp)),
            datetime.fromtimestamp(float(timestamp)),
        ]
    else:
        timestamp_low = timestamp_high = timestamp
        while len(timestamp_low) < 10:
            timestamp_low += "0"
            timestamp_high += "9"
        return [
            datetime.fromtimestamp(float(timestamp_low)),
            datetime.fromtimestamp(float(timestamp_high)),
        ]


def by_time(
    timestamp: str,
) -> re.Pattern:
    timestamp_str = timestamp.replace(".", "")
    b_timestamp = timestamp_str.encode("utf-8")
    pattern = re.compile(
        rb"-+\n-\s+\d+\s+%b\d*\s+NOK\s+IN\s+\w*+\s+\d+-\d+-\d+\s\d+:\d+:\d+.\d+.\d+"
        % (b_timestamp)
    )
    return pattern


def by_signal(signal_name: str) -> re.Pattern:
    b_signal_name = signal_name.encode("utf-8")
    return re.compile(
        rb"-+\n-\s+\d+\s+\d+\s+NOK\s+IN\s+\w*%b\w*+\s+\d+-\d+-\d+\s\d+:\d+:\d+.\d+.\d+"
        % (b_signal_name)
    )


def by_time_and_signal(
    timestamp: str,
    signal_name: str,
) -> re.Pattern:
    timestamp_str = timestamp.replace(".", "")
    b_timestamp = timestamp_str.encode("utf-8")
    b_signal_name = signal_name.encode("utf-8")
    pattern = re.compile(
        rb"-+\n-\s+\d+\s+%b\d*\s+NOK\s+IN\s+\w*%b\w*+\s+\d+-\d+-\d+\s\d+:\d+:\d+.\d+.\d+"
        % (b_timestamp, b_signal_name)
    )
    return pattern


from time import time


class PassClient:
    def __init__(self, root_dir: str, folders: str) -> None:
        self.root_dir = root_dir
        self.folders = folders
        self._txt_divider_header = re.compile(rb"(#\s*=+\n#\s+.*\n#\s+=+\n)")
        self._txt_divider_dashed = re.compile(rb"-+\n")
        self.metadata_regex = re.compile(
            rb"#\s*=+\n#\s+(\w+)\s+(\w+)=(\w+)\s+(\w+)=\w+\s+(\d+-\d+-\d+\s+\d+:\d+:\d+\s\w+)\s(\w+)\s=\s\"(\w+)\"\s(\w+)\s=\s\"(\w+)\"\s*\n#\s+=+\n"
        )
        self.header_regex = re.compile(
            rb"#\s*=+\n#\s+(\w+)\s+\|\s+(\w+\s\[\w+\])\s+\|\s+(\w+)\s+\|\s+(\w+)\s\|\s(\w+\s\w+)\s+\|\s+(\w+)\n#\s=+"
        )
        self._interlock_regex = re.compile(
            rb"-+\n-\s+\d+\s+\d+\s+NOK\s+IN\s+\w+\s+\d+-\d+-\d+\s\d+:\d+:\d+.\d+.\d+"
        )

    def get(
        self,
        area: Literal["MP", "G2", "G3", "O2"],
        signal_name: Optional[str] = None,
        timestamp: Optional[str] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        override_limit: bool = False,
    ) -> List[InterlockEventData] | None:

        header = None
        metadata = None

        if timestamp:
            pattern = by_time(timestamp=timestamp)
            start_datetime, end_datetime = timestamp_to_date_range(timestamp=timestamp)

            if signal_name:
                pattern = by_time_and_signal(
                    timestamp=timestamp, signal_name=signal_name
                )
        else:
            if not (start_datetime or end_datetime) and not override_limit:
                raise Exception(
                    "Please provide start date and end date when querying without timestamp. If you only provide one only results for that day will be returned."
                )
            elif start_datetime and end_datetime:
                if (
                    end_datetime - start_datetime
                    > timedelta(days=PASS_LOG_DAYS_QUERY_LIMIT)
                    and not override_limit
                ):
                    raise Exception(
                        f"Please don't query more than {PASS_LOG_DAYS_QUERY_LIMIT} days at once."
                    )
            if signal_name:
                pattern = by_signal(signal_name=signal_name)
            else:
                pattern = self._interlock_regex

        files = get_pass_files(
            folders=get_folders(folders=self.folders, area=area),
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            root_dir=self.root_dir,
        )

        for file in files:
            for event in self.search_file(file, pattern):
                yield event

    def search_file(
        self,
        file_path: str,
        pattern: re.Pattern,
    ):
        with open(file_path, mode="r", encoding="utf-8") as file_obj:
            with mmap.mmap(
                file_obj.fileno(), length=0, access=mmap.ACCESS_READ
            ) as mmap_obj:
                # Find the file header and extract the information. Later used as header for the dataframes
                b_header = self.header_regex.findall(mmap_obj)
                if b_header:
                    header = [x.decode(encoding="utf-8") for x in b_header[0]]

                # divide the file in chunks by the metadata blocks that seperate the interlock events
                chunks = self._txt_divider_header.split(mmap_obj)
                previous = b""
                for chunk in chunks:
                    # look for the search pattern in the chunk
                    if pattern.search(chunk):
                        # extract the metadata for the chunk
                        b_metadata = self.metadata_regex.findall(previous)
                        if b_metadata:
                            metadata = [
                                x.decode(encoding="utf-8") for x in b_metadata[0]
                            ]

                        # Extract the data by seperating the block below the header by the dotted line
                        data = [
                            x.decode(encoding="utf-8")
                            for x in self._txt_divider_dashed.split(chunk)
                        ]
                        event = pd.DataFrame()
                        pre_events = pd.DataFrame()
                        post_events = pd.DataFrame()
                        if data and header and metadata:
                            # Clean up data and conver to dataframes
                            data = list(filter(None, data))
                            dataframes = []
                            for i, block in enumerate(data):
                                data_list = [
                                    re.split(r"\s+", x) for x in block.split("\n")
                                ]
                                dataframes.append(pd.DataFrame(data_list))
                                dataframes[i][6] = (
                                    dataframes[i][6] + " " + dataframes[i][7]
                                )
                                dataframes[i].drop(columns=[0, 7], inplace=True)
                                dataframes[i].columns = header
                                dataframes[i].dropna(how="all", inplace=True)
                                event = dataframes[i].iloc[:1]
                                pre_events = None if i < 1 else dataframes[i - 1]
                                # Might want to also drop the interlock event from the post data
                                post_events = dataframes[i]
                            if not event.empty and not post_events.empty:
                                yield InterlockEventData(
                                    header=header,
                                    metadata=metadata,
                                    event=event,
                                    pre_events=pre_events,
                                    post_events=post_events,
                                )

                    previous = chunk
