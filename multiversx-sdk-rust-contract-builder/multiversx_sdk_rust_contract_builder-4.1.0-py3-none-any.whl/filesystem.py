import logging
from pathlib import Path
from typing import Callable, Union
from zipfile import ZIP_DEFLATED, ZipFile

from multiversx_sdk_rust_contract_builder.errors import ErrKnown


def archive_folder(archive_file: Path, folder: Path, should_include_file: Union[Callable[[Path], bool], None] = None):
    files = get_all_files(folder, should_include_file)

    with ZipFile(archive_file, "w", ZIP_DEFLATED) as archive:
        for full_path in files:
            archive.write(full_path, full_path.relative_to(folder))

    logging.info(f"Created archive: file = {archive_file}, with size = {archive_file.stat().st_size} bytes")


def get_all_files(folder: Path, should_include_file: Union[Callable[[Path], bool], None] = None):
    should_include_file = should_include_file or (lambda _: True)
    paths = list(folder.rglob("*"))
    paths = [path for path in paths if path.is_file() and should_include_file(path)]
    return paths


def find_file_in_folder(folder: Path, pattern: str) -> Path:
    files = list(folder.rglob(pattern))

    if len(files) == 0:
        raise ErrKnown(f"No file matches pattern [{pattern}] in folder {folder}")
    if len(files) > 1:
        logging.warning(f"More files match pattern [{pattern}] in folder {folder}. Will pick first:\n{files}")

    file = folder / files[0]
    return Path(file).resolve()
