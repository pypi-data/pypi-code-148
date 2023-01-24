import os
import re
import gzip
import logging
import pandas as pd
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def get_format(format: str):
    if format == "nginx":
        return re.compile(r"""(?P<remote_addr>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(?P<timestamp>\d{2}\/[a-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2} (\+|\-)\d{4})\] ((\"(GET|POST) )(?P<url>.+)(http\/1\.1")) (?P<status>\d{3}) (?P<bytes_sent>\d+) (["](?P<refferer>(\-)|(.+))["]) (["](?P<user_agent>.+)["])""", re.IGNORECASE)
    else:
        raise NotImplementedError(f"Format {format} not implemented")


def _parse(
    filepath: Union[str, bytes, os.PathLike],
    line_format: str
):
    items = []
    if str(filepath).endswith('.gz'):
        logger.info(f"Reading {filepath}")
        try:
            with gzip.open(filepath, 'rt', encoding='utf-8') as f:
                for line in f.readlines():
                    data = re.search(line_format, line)
                    if data is not None:
                        items.append(data.groupdict())
        except Exception as e:
            logger.error(f"[{e.__class__.__name__}] {e} for {filepath}")
    else:
        logger.info(f"Reading {filepath}")
        try:
            with filepath.open("r") as f:
                for line in f.readlines():
                    data = re.search(line_format, line)
                    if data is not None:
                        items.append(data.groupdict())
        except Exception as e:
            logger.error(f"[{e.__class__.__name__}] {e} for {filepath}")
    
    return items


def parse(
    filepath: Union[str, bytes, os.PathLike],
    format: str="nginx",
    date_format: str="%d/%b/%Y:%H:%M:%S %z"
):
    root = Path(filepath)
    line_format = get_format(format)

    items = []
    if root.is_dir():
        for filepath in root.iterdir():
            items.extend(_parse(filepath, line_format))
    else:
        logger.info(f"Reading {root}")
        items.extend(_parse(root, line_format))
    
    df = pd.DataFrame(items)
    df['timestamp'] = pd.to_datetime(
       df['timestamp'],
       format=date_format,
       utc=True)
    df = df.sort_values(by='timestamp')

    return df
