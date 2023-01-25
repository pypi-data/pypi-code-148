"""
Collector plugin for raw files
"""

import shutil

from pathlib import Path
from typing import Any, List
from urllib.parse import unquote, urljoin, urlparse

from packageurl import PackageURL  # type: ignore

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.net import download_file
from hoppr.result import Result


class CollectRawPlugin(SerialCollectorPlugin):
    """
    Collector plugin for raw files
    """

    supported_purl_types = ["binary", "generic", "raw"]
    products: List[str] = ["binary/*", "generic/*", "raw/*"]

    def get_version(self) -> str:
        return __version__

    @hoppr_rerunner
    def collect(self, comp: Any, repo_url: str, creds: CredObject = None):
        """
        Copy a component to the local collection directory structure
        """
        source_url = urlparse(repo_url)

        purl = PackageURL.from_string(comp.purl)
        result = self.check_purl_specified_url(purl, repo_url)
        if not result.is_success():
            return result

        subdir = None
        if purl.namespace is not None:
            source_url = urlparse(urljoin(source_url.geturl() + "/", purl.namespace))
            subdir = unquote(purl.namespace)

        target_dir = self.directory_for(purl.type, repo_url, subdir=subdir)

        file_name = unquote(purl.name)

        if source_url.scheme == "file":
            source_url = urlparse(repo_url + (purl.namespace or ""))
            source_file = Path(source_url.path, file_name).expanduser()

            self.get_logger().info(
                msg="Copying component:",
                indent_level=2,
            )

            self.get_logger().info(
                msg=f"source: {source_file}",
                indent_level=3,
            )

            self.get_logger().info(
                msg=f"destination: {target_dir.joinpath(file_name)}",
                indent_level=3,
            )

            if not source_file.is_file():
                msg = f"Unable to locate file {source_file}, skipping remaining attempts"
                self.get_logger().error(msg=msg, indent_level=2)
                return Result.fail(message=msg)

            shutil.copy(source_file, target_dir)
            return Result.success()

        download_url = urljoin(source_url.geturl() + "/", file_name)

        self.get_logger().info(
            msg="Downloading file:",
            indent_level=2,
        )

        self.get_logger().info(
            msg=f"source: {download_url}",
            indent_level=3,
        )

        self.get_logger().info(
            msg=f"destination: {target_dir.joinpath(file_name)}",
            indent_level=3,
        )

        response = download_file(download_url, target_dir.joinpath(file_name), creds)
        result = Result.from_http_response(response)

        if result.is_fail():
            msg = f"Unable to download from {download_url}, skipping remaining attempts"
            self.get_logger().error(msg=msg, indent_level=2)

        return result
