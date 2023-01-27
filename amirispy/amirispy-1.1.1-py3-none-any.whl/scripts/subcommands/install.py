# SPDX-FileCopyrightText: 2022 German Aerospace Center <amiris@dlr.de>
#
# SPDX-License-Identifier: Apache-2.0

import logging as log
import os
import shutil
from pathlib import Path

import pkg_resources

import wget
import zipfile

from amirispy.source.files import ensure_folder_exists
from amirispy.source.logs import log_and_print


def install_amiris(url: str, target_folder: Path) -> None:
    """
    Download and unzip AMIRIS from given url, add "fameSetup.yaml" and "log4j.properties"

    Args:
        url: where to download packaged AMIRIS file from
        target_folder: folder where to save the AMIRIS to
    """

    ensure_folder_exists(target_folder)
    download_file_path = Path(target_folder, "amiris.zip")
    wget.download(url, str(download_file_path))
    log.info(f"Downloaded file to {download_file_path}")

    if zipfile.is_zipfile(download_file_path):
        with zipfile.ZipFile(download_file_path, "r") as zip_ref:
            zip_ref.extractall(target_folder)
        os.remove(download_file_path)

        for file in target_folder.glob("target/*"):
            shutil.move(src=str(file), dst=target_folder)
        os.removedirs(Path(target_folder, "target"))

        log.info(f"Unzipped file content to {target_folder}")
    else:
        log.info("Downloaded file is not a zip file: Could not unzip")

    log.info(f"Copying standard configuration files to {target_folder}")
    resource_path = Path(pkg_resources.resource_filename("amirispy.scripts", "resources"))  # noqa

    shutil.copy(src=Path(resource_path, "fameSetup.yaml"), dst=Path(target_folder, "fameSetup.yaml"))

    log_and_print(f"AMIRIS installation to folder {target_folder} completed.")
