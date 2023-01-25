"""
Collector plugin for pypi images
"""
from __future__ import annotations

import importlib.util
import re
import sys

from subprocess import CalledProcessError
from urllib.parse import ParseResult, urljoin, urlparse

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component
from packageurl import PackageURL

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.context import Context
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.result import Result


class CollectPypiPlugin(SerialCollectorPlugin):
    """
    Collector plugin for pypi images
    """

    supported_purl_types = ["pypi"]
    required_commands = [sys.executable]
    products: list[str] = ["pypi/*"]
    system_repositories = ["https://pypi.org/simple"]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: Context, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.manifest_repos: list[str] = []
        self.password_list: list[str] = []
        self.base_command = [self.required_commands[0], "-m", "pip"]

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredObject | None = None) -> Result:
        """
        Copy a component to the local collection directory structure
        """
        if importlib.util.find_spec(name="pip") is None:
            return Result.fail(message="The pip package was not found. Please install and try again.")

        purl = PackageURL.from_string(comp.purl)
        result = self.check_purl_specified_url(purl, repo_url)  # type: ignore
        if not result.is_success():
            return result

        source_url = repo_url
        if not re.match(pattern="^.*simple/?$", string=source_url):
            source_url = urljoin(base=source_url, url="simple")

        password_list = []

        if creds is not None:
            parsed_url = urlparse(url=source_url)._asdict()
            parsed_url["netloc"] = f"{creds.username}:{creds.password}@{parsed_url['netloc']}"
            source_url = ParseResult(**parsed_url).geturl()
            password_list = [creds.password]

        target_dir = self.directory_for(purl.type, repo_url, subdir=f"{purl.name}_{purl.version}")

        self.get_logger().info(msg=f"Target directory: {target_dir}", indent_level=2)

        command = [
            *self.base_command,
            "download",
            "--no-deps",
            "--no-cache",
            "--timeout",
            "60",
            "--index-url",
            source_url,
            "--dest",
            f"{target_dir}",
            f"{purl.name}=={purl.version}",
        ]

        got_binary = False
        base_error_msg = f"Failed to download {purl.name} version {purl.version}"

        run_result = self.run_command([*command, "--only-binary=:all:"], password_list)

        try:
            run_result.check_returncode()
            got_binary = True
        except CalledProcessError:
            self.get_logger().debug(msg=f"{base_error_msg} binary package", indent_level=2)

        run_result = self.run_command([*command, "--no-binary=:all:"], password_list)

        try:
            run_result.check_returncode()
        except CalledProcessError:
            self.get_logger().debug(msg=f"{base_error_msg} source package", indent_level=2)
            if not got_binary:
                return Result.retry(f"{base_error_msg} as either whl or source.")

        return Result.success()
