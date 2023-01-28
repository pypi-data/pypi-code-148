"""utils for file handling"""
import os
import codecs
from typing import Union


def remove_bom_inplace(path: Union[str, os.PathLike, bytes]) -> None:
    """
    Removes BOM mark, if it exists, from a file and rewrites it in-place.
    :param path: Path to the file. Works with anything to use for open()
    """
    buffer_size = 4096
    bom_length = len(codecs.BOM_UTF8)

    with open(path, "rb") as input_file:
        chunk = input_file.read(buffer_size)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[bom_length:]
            while chunk:
                input_file.seek(i)
                input_file.write(chunk)
                i += len(chunk)
                input_file.seek(bom_length, os.SEEK_CUR)
                chunk = input_file.read(buffer_size)
            input_file.seek(-bom_length, os.SEEK_CUR)
            input_file.truncate()
