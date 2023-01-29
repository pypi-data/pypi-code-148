import glob
import os
import re
from datetime import datetime, timedelta
from typing import List, Literal, Optional


def get_folders(
    folders: List[str] | str, area: Literal["MP", "G2", "G3", "O2"]
) -> List[str]:
    folders_list = []
    result = []
    if isinstance(folders, str):
        folders_list = folders.split(",")
    else:
        folders_list = folders
    for folder in folders_list:
        if area in folder:
            result.append(folder)
    return result


def get_pass_file_by_date(d: datetime.date, folder: str):
    files = []

    files = files + glob.glob(
        r"*%s.txt" % (d.isoformat()),
        root_dir=folder,
    )

    return files


import pandas as pd


def get_pass_files(
    folders: List[str],
    root_dir: str,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
) -> List[str]:

    result = []
    all_files = []
    for folder in folders:
        folder = root_dir + folder
        if not start_datetime and not end_datetime:
            for file in os.listdir(folder):
                if file.endswith(".txt"):
                    if file not in all_files:
                        all_files.append(file)
                        file_path = os.path.join(folder, file)
                        if os.path.isfile(file_path):
                            result.append(file_path)
        else:
            files = []
            if not start_datetime or not end_datetime:
                datetime = start_datetime or end_datetime
                date = datetime.date()
                files = get_pass_file_by_date(date, folder=folder)
            else:
                dates = pd.date_range(start=start_datetime, end=end_datetime, freq="D")

                for date in dates:
                    files = files + get_pass_file_by_date(date.date(), folder=folder)
            if files:
                for file in files:
                    if file not in all_files:
                        all_files.append(file)
                        result.append(os.path.join(folder, file))

    return result


def get_files(
    folders: List[str] | str,
    system: Literal["tds", "tvs"],
    tcs_type: Literal["SlowControl", "TcsTrace"],
    root_dir: Optional[str] = None,
    start_datetime: Optional[datetime] = None,
    end_datetime: Optional[datetime] = None,
    area: Optional[Literal["G2", "G3", "O2"]] = None,
) -> List[str]:
    files = []
    files_found = []
    _folders = []
    if start_datetime > end_datetime:
        start_datetime, end_datetime = end_datetime, start_datetime
    date_delta = end_datetime.date() - start_datetime.date()
    if date_delta.days > 0:
        days = [
            start_datetime.date() + timedelta(days=i) for i in range(date_delta.days)
        ]
    else:
        days = [start_datetime.date()]
    if isinstance(folders, str):
        folders = folders.split(",")
    for folder in folders:
        if folder.find(area.lower()) != -1:
            _folders.append(folder)
    for day in days:
        for folder in _folders:
            if root_dir:
                folder = os.path.join(root_dir, folder)

            files = files + glob.glob(
                os.path.join(
                    folder,
                    tcs_type,
                    f"*{system.lower()}*{datetime.strftime(day, '%Y%m%d')}*",
                )
            )

    if files.count == 1:
        return files
    if not files:
        raise Exception(
            r"No files found! make sure the files are in $root_dir/path {area}/(TcsTrace/SlowControl)/*"
        )
    file_dict = {}
    for i, timestamp in enumerate(re.findall(r"\d{8}-\d{6}", "".join(files))):
        file_dict[datetime.strptime(timestamp, "%Y%m%d-%H%M%S")] = files[i]
    timestamps = list(file_dict.keys())
    closest_start_datetime = 0
    closest_end_datetime = len(timestamps)
    for index, timestamp in enumerate(sorted(timestamps)):
        if timestamp < start_datetime:
            closest_start_datetime = index
        if timestamp > end_datetime:
            closest_end_datetime = index
            break

    timestamps = timestamps[closest_start_datetime:closest_end_datetime]
    for t in timestamps:
        files_found.append(file_dict[t])
    return files_found
