"""
Collector plugin for helm charts
"""
import re

from copy import deepcopy
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urljoin

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component
from packageurl import PackageURL  # type: ignore

from hoppr import __version__, utils
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.context import Context
from hoppr.exceptions import HopprLoadDataError
from hoppr.flatten_sboms import flatten_sboms
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.hoppr_types.manifest_file_content import Repository
from hoppr.hoppr_types.purl_type import PurlType
from hoppr.result import Result


class CollectHelmPlugin(SerialCollectorPlugin):
    """
    Class to copy helm charts
    """

    supported_purl_types = ["helm"]
    required_commands = ["helm"]
    products: list[str] = ["helm/*"]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: Context, config: Optional[Dict] = None) -> None:
        super().__init__(context=context, config=config)

        self.create_logger()

        if self.config is not None:
            if "helm_command" in self.config:
                self.required_commands = [self.config["helm_command"]]

        self.base_command = [self.required_commands[0], "fetch"]

        system_repos_file = Path.home() / ".config" / "helm" / "repositories.yaml"
        if not self.context.strict_repos and system_repos_file.exists():
            system_repos: list[dict[str, str]] = []

            try:
                system_repos_dict = utils.load_file(input_file_path=system_repos_file)
                if not isinstance(system_repos_dict, dict):
                    raise HopprLoadDataError("Incorrect format.")

                system_repos = system_repos_dict["repositories"]
            except HopprLoadDataError as ex:
                self.get_logger().warning(msg=f"Unable to parse Helm repositories file ({system_repos_file}): '{ex}'")

            self.context.manifest.consolidated_repositories[PurlType.HELM].extend(
                [Repository(url=repo["url"], description=repo["name"]) for repo in system_repos]
            )

            self.context.consolidated_sbom = flatten_sboms(self.context.manifest)
            self.context.delivered_sbom = deepcopy(self.context.consolidated_sbom)

    @hoppr_rerunner
    # pylint: disable=duplicate-code
    def collect(self, comp: Component, repo_url: str, creds: Optional[CredObject] = None):
        """
        Collect helm chart
        """

        purl = PackageURL.from_string(comp.purl)

        if self.context.strict_repos:
            helm_result = self.check_purl_specified_url(purl, repo_url)  # type: ignore
            if not helm_result.is_success():
                return helm_result

        if not re.match(pattern="^.*/$", string=repo_url):
            repo_url = f"{repo_url}/"

        target_dir = self.directory_for(purl.type, repo_url, subdir=f"{purl.name}_{purl.version}")

        for subdir in ["", purl.name]:
            source_url = urljoin(base=repo_url, url=subdir)

            self.get_logger().info(msg="Fetching helm chart:", indent_level=2)
            self.get_logger().info(msg=f"source: {source_url}", indent_level=3)
            self.get_logger().info(msg=f"destination: {target_dir}", indent_level=3)

            command = [
                *self.base_command,
                "--repo",
                source_url,
                "--destination",
                f"{target_dir}",
                purl.name,
                "--version",
                purl.version,
            ]

            password_list = []

            if creds is not None:
                command = [
                    *command,
                    "--username",
                    creds.username,
                    "--password",
                    creds.password,
                ]

                password_list = [creds.password]

            run_result = self.run_command(command, password_list)

            if run_result.returncode == 0:
                self.get_logger().info(f"Complete helm chart artifact copy for {purl.name} version {purl.version}")
                return Result.success()

        msg = f"Failed to download {purl.name} version {purl.version} helm chart"
        self.get_logger().debug(msg=msg, indent_level=2)
        return Result.retry(msg)
