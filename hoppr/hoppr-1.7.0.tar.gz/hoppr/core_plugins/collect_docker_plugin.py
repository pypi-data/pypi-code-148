"""
Collector plugin for docker images
"""

import os
import re
import urllib.parse

from typing import Any, Dict, List, Optional

from packageurl import PackageURL

from hoppr import __version__
from hoppr.base_plugins.collector import SerialCollectorPlugin
from hoppr.base_plugins.hoppr import hoppr_rerunner
from hoppr.context import Context
from hoppr.hoppr_types.cred_object import CredObject
from hoppr.result import Result


class CollectDockerPlugin(SerialCollectorPlugin):
    """
    Collector plugin for docker images
    """

    supported_purl_types = ["docker"]
    required_commands = ["skopeo"]
    products: List[str] = ["docker/*"]
    system_repositories = ["https://docker.io/"]

    def get_version(self) -> str:  # pylint: disable=duplicate-code
        return __version__

    def __init__(self, context: Context, config: Optional[Dict] = None) -> None:
        super().__init__(context=context, config=config)
        if self.config is not None:
            if "skopeo_command" in self.config:
                self.required_commands = [self.config["skopeo_command"]]

    @hoppr_rerunner
    def collect(self, comp: Any, repo_url: str, creds: Optional[CredObject] = None):
        """
        Copy a component to the local collection directory structure
        """
        purl = PackageURL.from_string(comp.purl)
        docker_result = self.check_purl_specified_url(purl, repo_url)  # type: ignore
        if not docker_result.is_success():
            return docker_result

        source_image = os.path.join(repo_url, purl.namespace or "", purl.name + ":" + purl.version)
        source_image = re.sub(r"^https?://", "", source_image)
        if not source_image.startswith("docker://"):
            source_image = "docker://" + source_image

        file_name = urllib.parse.unquote(purl.name) + "_" + purl.version
        target_dir = self.directory_for(purl.type, repo_url, subdir=purl.namespace)
        target_path = os.path.join(target_dir, file_name)
        destination = "docker-archive:" + target_path

        self.get_logger().info(
            msg="Copying docker image:",
            indent_level=2,
        )

        self.get_logger().info(
            msg=f"source: {source_image}",
            indent_level=3,
        )

        self.get_logger().info(
            msg=f"destination: {destination}",
            indent_level=3,
        )

        command = [self.required_commands[0], "copy"]

        password_list = []
        if creds is not None:
            password_list = [creds.password]
            command.extend(["--src-creds", f"{creds.username}:{creds.password}"])

        if re.match("^http://", repo_url):
            command.append("--src-tls-verify=false")

        command.extend([source_image, destination])

        proc = self.run_command(command, password_list)

        if proc.returncode != 0:
            msg = f"Skopeo failed to copy docker image to {destination}, " + f"return_code={proc.returncode}"

            self.get_logger().debug(msg=msg, indent_level=2)

            if os.path.exists(target_path):
                self.get_logger().info(
                    msg="Artifact collection failed, deleting file and retrying",
                    indent_level=2,
                )
                os.remove(target_path)

            return Result.retry(message=msg)

        self.set_collection_params(comp, repo_url, target_dir)

        return Result.success(return_obj=comp)
