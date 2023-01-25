"""
Collector plugin for apt packages
"""
import fnmatch
import os
import shutil

from configparser import ConfigParser
from os import PathLike
from pathlib import Path
from subprocess import CalledProcessError
from typing import Dict, List, Mapping, Optional, Set, Tuple, Union
from urllib.parse import urlparse

import jc  # type: ignore

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component
from packageurl import PackageURL  # type: ignore

from hoppr import __version__
from hoppr.base_plugins.collector import BatchCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_process, hoppr_rerunner
from hoppr.configs.credentials import Credentials
from hoppr.context import Context
from hoppr.exceptions import HopprPluginError
from hoppr.hoppr_types.manifest_file_content import Repository
from hoppr.hoppr_types.purl_type import PurlType
from hoppr.result import Result


class CollectAptPlugin(BatchCollectorPlugin):
    """
    Collector plugin for apt packages
    """

    required_commands: List[str] = ["apt", "apt-cache"]
    supported_purl_types: List[str] = ["deb"]
    products: List[str] = ["deb/*"]

    def __init__(
        self,
        context: Context,
        config: Optional[Dict] = None,
        config_dir: Union[str, PathLike] = Path.cwd().joinpath(".hoppr-apt"),
    ) -> None:
        super().__init__(
            context=context,
            config=config,
        )

        self.manifest_repos: List[str] = []

        self.manifest_repos = [repo.url for repo in self.context.manifest.consolidated_repositories[PurlType.DEB]]

        proxy_args = self._repo_proxy()
        self.config_dir = Path(config_dir)

        self.apt_paths_dict: Mapping[str, Mapping] = {
            "etc": {
                "apt": {"auth.conf": None, "sources.list": None, "sources.list.d": {}},
                "cache": {"apt": {"archives": {"lock": None, "partial": {}}}},
            },
            "var": {
                "lib": {
                    "apt": {"lists": {"lock": None, "partial": {}}},
                    "dpkg": {"lock-frontend": None, "status": None},
                }
            },
        }

        self.base_command = [
            self.required_commands[0],
            f"--option=Dir={self.config_dir}",
            f"--option=Dir::State::status={self.config_dir / 'var' / 'lib' / 'dpkg' / 'status'}",
            *proxy_args,
        ]

    def _artifact_string(self, purl: PackageURL) -> str:
        artifact_string = purl.name

        if purl.qualifiers.get("arch") is not None:
            artifact_string = ":".join([artifact_string, purl.qualifiers.get("arch")])
        if purl.version is not None:
            artifact_string = "=".join([artifact_string, purl.version])

        return artifact_string

    def _download_component(self, purl: str) -> None:
        artifact = self._artifact_string(purl)  # type: ignore

        try:
            # Download the component
            download_result = self.run_command(
                [
                    *self.base_command,
                    "download",
                    artifact,
                ]
            )

            download_result.check_returncode()
        except CalledProcessError as ex:
            raise ex

    def _get_component_download_info(self, purl: PackageURL) -> Tuple[str, str]:
        artifact = self._artifact_string(purl=purl)  # type: ignore

        try:
            # Try getting component download URL
            url_result = self.run_command(
                [
                    *self.base_command,
                    "--print-uris",
                    "download",
                    artifact,
                ]
            )

            url_result.check_returncode()

            if len(url_result.stdout.decode("utf-8")) == 0:
                raise HopprPluginError
        except (CalledProcessError, HopprPluginError) as ex:
            msg = f"Failed to get download URL for component: '{purl}'"
            self.get_logger().debug(msg=msg, indent_level=2)
            raise ex

        # Take the first URL and download filename if multiple are returned
        # Apt download output format:
        #   '<download URL>' <URL-encoded download filename> <download size> SHA512:<package hash>
        # Extract the output into a tuple of the form (<download URL>, <URL-encoded download filename>). For example:
        #   ("http://archive.ubuntu.com/ubuntu/pool/main/g/git/git_2.34.1-1ubuntu1.5_amd64.deb",
        #    "git_1%3a2.34.1-1ubuntu1.5_amd64.deb")
        result = url_result.stdout.decode("utf-8").split("\n")[0]
        found_url, download_filename = result.split(" ")[0:2]

        self.get_logger().debug(msg=f"Found URL: {found_url}", indent_level=3)
        self.get_logger().debug(msg=f"Download filename: {download_filename}", indent_level=3)

        return found_url.strip("'"), download_filename

    def _get_download_url_path(self, purl: PackageURL) -> str:
        """
        Get the path segment of the component download URL using `apt-cache show`
        """
        artifact = self._artifact_string(purl)  # type: ignore

        command = ["apt-cache", "show", artifact]

        cmd_result = self.run_command(command)

        try:
            cmd_result.check_returncode()
        except CalledProcessError as ex:
            raise ex

        pkg_info = jc.parse(parser_mod_name="ini", data=cmd_result.stdout.decode(encoding="utf-8"))

        if not isinstance(pkg_info, dict) or not isinstance(pkg_info["Filename"], str):
            raise TypeError("Parsed output not in the expected format.")

        return pkg_info["Filename"]

    def _get_found_repo(self, found_url: str) -> Optional[str]:
        """
        Identify the repository associated with the specified URL
        """
        for repo in self.manifest_repos:
            if found_url.startswith(repo):
                return repo

        return None

    def _populate_apt_folder_structure(self, apt_path: Path, path_dict: Mapping[str, Optional[Mapping]]) -> None:
        for key, value in path_dict.items():
            # None type indicates file to create
            if value is None:
                apt_file = apt_path / key
                apt_file.touch(exist_ok=True, mode=0o644)
            # Dict type indicates directory to create
            elif isinstance(value, Dict):
                apt_dir = apt_path / key
                apt_dir.mkdir(exist_ok=True, parents=True)

                if len(value.items()) > 0:
                    self._populate_apt_folder_structure(apt_path=apt_dir, path_dict=value)
            else:
                raise TypeError("Value is not expected type.")

    def _populate_auth_conf(self, repo_list: List[Repository], file: Path) -> None:
        """
        Populate Apt authentication config file
        """
        creds = []
        for repo in repo_list:
            repo_credentials = Credentials.find_credentials(repo.url)
            if repo_credentials is not None:
                creds.append(
                    f"machine {urlparse(repo.url).netloc} "
                    f"login {repo_credentials.username} "
                    f"password {repo_credentials.password}\n"
                )

        # Set restrictive permissions on Apt authentication config file
        file.chmod(mode=0o600)

        with file.open(mode="w+", encoding="utf-8") as auth_conf:
            auth_conf.write("\n".join(creds))

    def _populate_sources_list(self, repo_list: List[str], file: Path) -> None:
        """
        Populate sources list
        """
        # Read data from /etc/os-release file
        parser = ConfigParser()

        with (Path("/") / "etc" / "os-release").open(mode="r", encoding="utf-8") as os_release:
            parser.read_string(string=f"[os-release]\n{os_release.read()}")

        version_codename = parser["os-release"]["VERSION_CODENAME"]

        sources = []
        for repo in repo_list:
            for component in ["main restricted", "universe", "multiverse"]:
                sources.append(f"deb {repo} {version_codename} {component}")
                sources.append(f"deb {repo} {version_codename}-updates {component}")
                sources.append(f"deb {repo} {version_codename}-security {component}")

        with file.open(mode="w+", encoding="utf-8") as sources_list:
            sources_list.write("\n".join(sources))

    def _repo_proxy(self) -> Set[str]:
        proxy_args: List[str] = []

        for proto in ["http", "https"]:
            proxy = os.getenv(f"{proto}_proxy")
            if proxy:
                proxy_args = [*proxy_args, f"--option=Acquire::{proto}::Proxy={proxy}"]

        no_proxy_urls = [item for item in os.getenv("no_proxy", "").split(",") if item != ""]

        for url in self.manifest_repos:
            parsed_url = urlparse(url)

            for pattern in no_proxy_urls:
                # Check if pattern is a substring or wildcard match of manifest repo URL
                if pattern in parsed_url.netloc or fnmatch.fnmatch(name=parsed_url.netloc, pat=pattern):
                    proxy_args = [
                        *proxy_args,
                        f"--option=Acquire::http::Proxy::{parsed_url.netloc}=DIRECT",
                        f"--option=Acquire::https::Proxy::{parsed_url.netloc}=DIRECT",
                    ]

        return set(proxy_args)

    def get_version(self) -> str:
        return __version__

    @hoppr_process
    def pre_stage_process(self) -> Result:
        self._populate_apt_folder_structure(apt_path=self.config_dir, path_dict=self.apt_paths_dict)

        self._populate_sources_list(
            repo_list=self.manifest_repos,
            file=self.config_dir / "etc" / "apt" / "sources.list",
        )

        self._populate_auth_conf(
            repo_list=self.context.manifest.consolidated_repositories[PurlType.DEB],
            file=self.config_dir / "etc" / "apt" / "auth.conf",
        )

        if not self.context.strict_repos:
            system_apt_path = Path("/") / "etc" / "apt"
            plugin_apt_path = self.config_dir / "etc" / "apt"

            # Copy system Apt source lists into temporary directory
            shutil.copyfile(
                src=system_apt_path / "sources.list",
                dst=plugin_apt_path / "sources.list.d" / "system.list",
            )

            shutil.copytree(
                src=system_apt_path / "sources.list.d",
                dst=plugin_apt_path / "sources.list.d",
                dirs_exist_ok=True,
            )

        # Populate user Apt cache
        result = self.run_command(
            [
                *self.base_command,
                "--option=Dir::Etc::trusted=/etc/apt/trusted.gpg",
                "--option=Dir::Etc::trustedparts=/etc/apt/trusted.gpg.d",
                "update",
            ]
        )

        if result.returncode != 0:
            return Result.fail("Failed to populate Apt cache.")

        return Result.success()

    @hoppr_rerunner
    def collect(self, comp: Component) -> Result:
        """
        Copy a component to the local collection directory structure
        """

        purl = PackageURL.from_string(comp.purl)

        try:
            found_url, download_filename = self._get_component_download_info(purl=purl)  # type: ignore
        except (CalledProcessError, HopprPluginError) as ex:
            return Result.retry(message=str(ex))

        download_url_path = Path(self._get_download_url_path(purl=purl))  # type: ignore
        subdir = download_url_path.parent

        if self.context.strict_repos:
            # Strip surrounding single quotes to compare against manifest repos
            repo = self._get_found_repo(found_url)

            # Return failure if found APT URL is not from a repo defined in the manifest
            if repo is None:
                return Result.fail(
                    f"Apt download URL does not match any repository in manifest. (Found URL: '{found_url}')"
                )

            result = self.check_purl_specified_url(purl, repo)  # type: ignore
            if not result.is_success():
                return result
        else:
            # Default to found_url with the path component removed
            repo = found_url.removesuffix(str(download_url_path))

        target_dir = self.directory_for(purl.type, repo, subdir=str(subdir))

        try:
            self._download_component(purl=purl)  # type: ignore
        except CalledProcessError:
            msg = f"Failed to download Apt artifact {purl.name} version {purl.version}"
            return Result.retry(msg)

        self.get_logger().info(msg="Moving downloaded component:", indent_level=2)
        self.get_logger().info(msg=f"source: {download_filename}", indent_level=3)
        self.get_logger().info(msg=f"destination: {target_dir}", indent_level=3)

        shutil.move(src=download_filename, dst=target_dir)

        self.set_collection_params(comp, repo, target_dir)

        return Result.success(return_obj=comp)
