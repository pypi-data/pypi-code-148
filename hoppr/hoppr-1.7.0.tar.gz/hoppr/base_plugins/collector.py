"""
Base class for all collector plugins
"""

import json
import socket

from abc import abstractmethod
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Union, final
from urllib.parse import urlparse

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component, Property
from packageurl import PackageURL  # type: ignore

from hoppr import __version__, constants, plugin_utils
from hoppr.base_plugins.hoppr import HopprPlugin, hoppr_process, hoppr_rerunner
from hoppr.configs.credentials import Credentials
from hoppr.hoppr_types.bom_access import BomAccess
from hoppr.hoppr_types.component_coverage import ComponentCoverage
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.hoppr_types.purl_type import PurlType
from hoppr.result import Result
from hoppr.utils import dedup_list, remove_empty


class BaseCollectorPlugin(HopprPlugin):
    """
    Base class for collector plugins
    """

    default_component_coverage = ComponentCoverage.EXACTLY_ONCE
    bom_access = BomAccess.COMPONENT_ACCESS
    system_repositories: list[str] = []

    def _get_repos(self, comp: Component) -> list[str]:
        """
        Returns all repos listed in all BOM_PROPS_COMPONENT_SEARCH_SEQUENCE properties for this component
        """
        repo_list = []

        for prop in comp.properties or []:
            if prop.name == constants.BomProps.COMPONENT_SEARCH_SEQUENCE:
                search_sequence = json.loads(prop.value or "")
                repo_list.extend(search_sequence.get("Repositories", []))

        if not self.context.strict_repos:
            repo_list.extend(self.system_repositories)

        return dedup_list(repo_list)

    def directory_for(
        self,
        purl_type: Union[str, PurlType],
        repo_url: str,
        subdir: Union[str, None] = None,
    ) -> Path:
        """
        Identify the directory into which the artifact should be copied
        """

        repo_dir = plugin_utils.dir_name_from_repo_url(repo_url)
        directory = Path(self.context.collect_root_dir, str(purl_type), repo_dir)

        if subdir is not None:
            directory = Path(directory, subdir)

        directory.mkdir(parents=True, exist_ok=True)

        return directory

    @staticmethod
    def _parse_url_for_comparison(url: str) -> tuple[str, str, str]:
        """
        Resulting tuple is (host, port, path)
        """
        if url.startswith("file:") or "//" in url:
            initial_parse = urlparse(url)
        else:
            initial_parse = urlparse("//" + url)

        host_data = initial_parse.netloc.split(":")

        host = host_data[0]

        if len(host_data) > 1:
            port = host_data[1]
        elif initial_parse.scheme == "":
            port = ""
        else:
            port = str(socket.getservbyname(initial_parse.scheme))

        path = initial_parse.path.rstrip("/")

        return (host, port, path)

    @staticmethod
    def check_purl_specified_url(purl: PackageURL, repo_url: str) -> Result:
        """
        Test if a repository_url specified as a purl qualifier is a mis-match with a given repo_url

        If no repository_url is specified, repo_url is fine, no-mismatch, return False

        Otherwise, considered a match if repo_url starts with the purl url (after trimming trailing
        "/"s and URL scheme, if present)
        """
        purl_url = purl.qualifiers.get("repository_url")
        if purl_url is None:
            return Result.success()

        parsed_purl_url = BaseCollectorPlugin._parse_url_for_comparison(purl_url)
        parsed_repo_url = BaseCollectorPlugin._parse_url_for_comparison(repo_url)
        if (
            parsed_repo_url[0] == parsed_purl_url[0]
            and (not parsed_purl_url[1] or parsed_repo_url[1] == parsed_purl_url[1])
            and parsed_repo_url[2].startswith(parsed_purl_url[2])
        ):
            return Result.success()

        return Result.fail(f"Purl-specified repository url ({purl_url}) does not match current repo ({repo_url}).")

    def set_collection_params(self, comp: Component, repository: str, directory: Union[Path, str]) -> None:
        """
        Set collection parameters on sbom component
        """

        rel_dir = str(Path(directory).relative_to(self.context.collect_root_dir))

        collect_props: dict[str, str] = {
            constants.BomProps.COLLECTION_REPOSITORY: repository,
            constants.BomProps.COLLECTION_DIRECTORY: rel_dir,
            constants.BomProps.COLLECTION_PLUGIN: type(self).__name__,
            constants.BomProps.COLLECTION_TIMETAG: str(datetime.now(timezone.utc)),
        }

        if comp.properties is None:
            comp.properties = []

        for prop in comp.properties:
            if prop.name in collect_props:
                prop.value = collect_props.pop(prop.name)

        for key, value in collect_props.items():
            if value is not None:
                comp.properties.append(Property(name=key, value=value))


class SerialCollectorPlugin(BaseCollectorPlugin):
    """
    Base class for multi-process collector plugins
    """

    @abstractmethod
    @hoppr_rerunner
    def collect(self, comp: Any, repo_url: str, creds: Union[CredObject, None] = None):
        """
        This method should attempt to collect a single component from the specified URL
        """

    @final
    @hoppr_process
    def process_component(self, comp: Component) -> Result:
        """
        Copy a component to the local collection directory structure

        A CollectorPlugin will never return a RETRY result, but handles the retry logic internally.
        """

        logger = self.get_logger()

        result = Result.fail(f"No repository found for purl {comp.purl}")

        # for repo_url in self.context.manifest.get_repos():
        for repo_url in self._get_repos(comp):
            logger.info(f"Repository: {repo_url}")

            repo_creds = Credentials.find_credentials(repo_url)
            result = self.collect(comp, repo_url, repo_creds)

            if result.is_success():
                break  ### We found it, no need to try any more repositories

        return result

    @hoppr_process
    def post_stage_process(self):
        for purl_type in self.supported_purl_types:
            directory = Path(self.context.collect_root_dir, purl_type)

            if directory.is_dir():
                remove_empty(directory)

        return Result.success()


class BatchCollectorPlugin(BaseCollectorPlugin):
    """
    Base class for single-process collector plugins
    """

    config_file: Path

    @abstractmethod
    @hoppr_rerunner
    def collect(self, comp: Component):
        """
        This method should attempt to collect all components
        from all manifest repositories or registries that were
        previously configured in the pre stage process.

        Use of a single batch operation (i.e. dynamically constructed
        shell command) is encouraged if supported by the underlying
        collection tool(s).
        """

    @final
    @hoppr_process
    def process_component(self, comp: Component) -> Result:
        """
        Copy a component to the local collection directory structure

        A CollectorPlugin will never return a RETRY result, but handles the retry logic internally.
        """
        logger = self.get_logger()
        logger.info(f"Processing component {comp.purl}")

        return self.collect(comp)
