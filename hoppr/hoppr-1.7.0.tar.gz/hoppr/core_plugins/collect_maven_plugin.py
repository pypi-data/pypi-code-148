"""
Collector plugin for maven artifacts
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from subprocess import CalledProcessError
from tempfile import NamedTemporaryFile
from typing import Any, OrderedDict

import jmespath  # type: ignore[import]
import xmltodict  # type: ignore[import]

from hoppr_cyclonedx_models.cyclonedx_1_4 import Component
from packageurl import PackageURL  # type: ignore[import]

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.context import Context
from hoppr.flatten_sboms import flatten_sboms
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.hoppr_types.manifest_file_content import Repository
from hoppr.hoppr_types.purl_type import PurlType
from hoppr.result import Result

_MAVEN_DEP_PLUGIN = "org.apache.maven.plugins:maven-dependency-plugin:3.4.0"


class CollectMavenPlugin(SerialCollectorPlugin):
    """
    Collector plugin for maven artifacts
    """

    supported_purl_types = ["maven"]
    required_commands = ["mvn"]
    products: list[str] = ["maven/*"]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: Context, config: dict | None = None) -> None:
        super().__init__(context=context, config=config)

        self.extra_opts: list[str] = []

        if self.config is not None:
            self.required_commands = self.config.get("maven_command", self.required_commands)
            self.extra_opts = self.config.get("maven_opts", self.extra_opts)

        system_settings_file = Path("/") / "etc" / "maven" / "settings.xml"
        user_settings_file = Path.home() / ".m2" / "settings.xml"

        if not self.context.strict_repos:
            # Add system repositories to manifest
            for settings_file in [system_settings_file, user_settings_file]:
                if settings_file.is_file():
                    settings_dict: OrderedDict[str, Any] = xmltodict.parse(
                        settings_file.read_text(encoding="utf-8"),
                        encoding="utf-8",
                        force_list={"profile", "repository"},
                    )

                    repo_urls: list[str] = jmespath.search(
                        expression="settings.profiles.profile[].repositories.repository[].url",
                        data=settings_dict,
                    )

                    for repo_url in repo_urls:
                        self.context.manifest.consolidated_repositories[PurlType.MAVEN].append(
                            Repository(url=repo_url, description="")
                        )

                self.context.consolidated_sbom = flatten_sboms(self.context.manifest)
                self.context.delivered_sbom = deepcopy(self.context.consolidated_sbom)

    def _get_maven_component(self, command: list[str], password_list: list[str], **kwargs):
        for key, value in kwargs.items():
            command.append(f"-D{key}={value}")

        return self.run_command(command, password_list)

    @hoppr_rerunner
    def collect(self, comp: Component, repo_url: str, creds: CredObject | None = None) -> Result:
        """
        Copy a component to the local collection directory structure
        """
        # pylint: disable=too-many-locals

        purl = PackageURL.from_string(comp.purl)
        artifact = f"{purl.namespace}:{purl.name}:{purl.version}"

        if self.context.strict_repos:
            result = self.check_purl_specified_url(purl, repo_url)  # type: ignore
            if not result.is_success():
                return result

        extension = purl.qualifiers.get("type", "tar.gz")
        target_dir = self.directory_for(purl.type, repo_url, subdir=f"{purl.namespace}")

        self.get_logger().info(msg="Copying maven artifact:", indent_level=2)
        self.get_logger().info(msg=f"source: {repo_url}", indent_level=3)
        self.get_logger().info(msg=f"destination: {target_dir}", indent_level=3)

        settings_dict = {
            "settings": {
                "servers": {
                    "server": {
                        "id": "repoId",
                        "username": "${repo.login}",
                        "password": "${repo.pwd}",
                    }
                }
            }
        }

        with NamedTemporaryFile(mode="w+", encoding="utf-8") as settings_file:
            settings_file.write(xmltodict.unparse(input_dict=settings_dict, pretty=True))
            settings_file.flush()

            password_list = []

            defines = {
                "artifact": artifact,
                "dest": f"{target_dir}/{purl.name}-{purl.version}.{extension}",
                "packaging": f"{extension}",
                "remoteRepositories": f"repoId::::{repo_url}",
            }

            if creds is not None:
                defines["repo.login"] = creds.username
                defines["repo.pwd"] = creds.password
                password_list = [creds.password]

            command = [
                self.required_commands[0],
                f"{_MAVEN_DEP_PLUGIN}:get",
                f"--settings={settings_file.name}",
                *self.extra_opts,
            ]

            run_result = self._get_maven_component(command, password_list, **defines)
            error_msg = f"Failed to download maven artifact {artifact} type={extension}"

            try:
                run_result.check_returncode()

                if extension != "pom":
                    defines["packaging"] = "pom"
                    defines["dest"] = defines["dest"].replace(f".{extension}", ".pom")

                    error_msg = f"Failed to download pom for maven artifact {artifact}"
                    run_result = self._get_maven_component(command, password_list, **defines)
                    run_result.check_returncode()
            except CalledProcessError:
                self.get_logger().debug(msg=error_msg, indent_level=2)
                return Result.retry(message=error_msg)

        return Result.success()
