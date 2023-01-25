"""
Manifest business logic
"""
# Enable forward references
from __future__ import annotations

from pathlib import Path
from typing import Optional

from hoppr_cyclonedx_models.cyclonedx_1_3 import CyclonedxSoftwareBillOfMaterialSpecification as Bom_1_3  # type: ignore
from hoppr_cyclonedx_models.cyclonedx_1_4 import CyclonedxSoftwareBillOfMaterialsStandard as Bom_1_4  # type: ignore
from typer import echo

from hoppr import net, oci_artifacts, utils
from hoppr.exceptions import HopprLoadDataError
from hoppr.hoppr_types.manifest_file_content import ManifestFileContent, Repositories, SBOMRef
from hoppr.hoppr_types.purl_type import PurlType
from hoppr.utils import dedup_list


class Manifest:
    """Manifest business logic class

    Attributes
    ----------
    manifest_location: str | Path
        Path object representing a local manifest
        file or string representing manifest URL
    manifest_file_content: ManifestFileContent
        Populated ManifestFileContent object
    sboms: list[Bom_1_4 | Bom_1_3]
        List of SBOM objects contained in this manifest
    parent: Optional[Manifest]
        Manifest that includes this manifest file
    children: list[Manifest]
        Manifests that are included by this manifest file
    consolidated_repositories: Repositories
        Mapping of PURL types to repositories outlined in the manifest file
    """

    loaded_manifests: list[str] = []

    def __init__(self, manifest_location: str | Path = "") -> None:
        self.manifest_location: str | Path = manifest_location
        self.manifest_file_content: ManifestFileContent
        self.sboms: list[Bom_1_4 | Bom_1_3] = []
        self.parent: Optional[Manifest] = None
        self.children: list[Manifest] = []
        self.consolidated_repositories: Repositories

    @staticmethod
    def merge_repositories(first: Repositories, second: Repositories):
        """
        Add repos
        """
        combined: Repositories = {}
        for purl_type in PurlType:
            combined[purl_type] = dedup_list(first[purl_type] + second[purl_type])

        return combined

    @staticmethod
    def load_file(file: Path, parent: Optional[Manifest] = None) -> Manifest:
        """Creates a Manifest object from a local file

        Parameters
        ----------
        file : Path
            Relative or absolute path to manifest file
        parent : Optional[Manifest], optional
            Parent Manifest object, by default None

        Returns
        -------
        Manifest
            Manifest object representing the loaded manifest file
        """
        Manifest.loaded_manifests.append(str(file.resolve()))

        input_dict = utils.load_file(file)
        if not isinstance(input_dict, dict):
            raise HopprLoadDataError("Failed to parse manifest file as dictionary")

        manifest = Manifest(manifest_location=file.resolve())
        manifest.populate(input_dict, parent)
        return manifest

    @staticmethod
    def load_url(url: str, parent: Optional[Manifest] = None) -> Manifest:
        """Creates a manifest object from a URL

        Parameters
        ----------
        url : str
            URL of the manifest file
        parent : Optional[Manifest], optional
            Parent Manifest object, by default None

        Returns
        -------
        Manifest
            Manifest object representing the loaded manifest file
        """
        Manifest.loaded_manifests.append(url)

        input_dict = net.load_url(url)
        if not isinstance(input_dict, dict):
            raise HopprLoadDataError("Failed to parse manifest file as dictionary")

        manifest = Manifest(manifest_location=url)
        manifest.populate(input_dict, parent)
        return manifest

    def load_sbom(self, sbom_location: SBOMRef) -> Bom_1_4 | Bom_1_3:
        """Loads an SBOM from a URL or a local file

        Parameters
        ----------
        sbom_location : SBOMRef
            Location of SBOM file

        Returns
        -------
        Bom_1_4 | Bom_1_3
            A CycloneDX SBOM object representing the file content

        Raises
        ------
        HopprLoadDataError
            Unsupported SBOM location type or spec version
        """
        if sbom_location.local is not None:
            sbom_file_path = Path(self.manifest_location).parent.joinpath(sbom_location.local)
            sbom_file_object = utils.load_file(sbom_file_path)
        elif sbom_location.url is not None:
            sbom_file_object = net.load_url(sbom_location.url)
        elif sbom_location.oci is not None:
            sbom_file_object = oci_artifacts.pull_artifact(sbom_location.oci, allow_version_discovery=True)
        else:
            raise HopprLoadDataError(f"Unsupported SBOM Location {sbom_location}")

        if not isinstance(sbom_file_object, dict):
            raise HopprLoadDataError("Failed to parse manifest file as dictionary")

        spec_version = sbom_file_object.get("specVersion", "")

        if spec_version == "1.4":
            return Bom_1_4(**sbom_file_object)
        if spec_version == "1.3":
            return Bom_1_3(**sbom_file_object)
        raise HopprLoadDataError(f"{sbom_location} is an unknown spec version ({spec_version})")

    def build_repository_search(self) -> None:
        """
        Builds the computed repository search sequence for a parent and child manifest
        """
        if self.parent is None:
            self.consolidated_repositories = self.manifest_file_content.repositories
        else:
            self.consolidated_repositories = self.merge_repositories(
                self.parent.consolidated_repositories,
                self.manifest_file_content.repositories,
            )

    def populate(self, input_dict: dict, parent: Optional[Manifest] = None):
        """Populates Manifest object with dictionary contents

        Parameters
        ----------
        input_dict : dict
            A dictionary of manifest properties
        parent : Optional[Manifest], optional
            Parent Manifest object, by default None
        """

        self.manifest_file_content = ManifestFileContent(**input_dict)
        self.parent = parent

        if self.manifest_file_content is not None:
            for sbom_ref in self.manifest_file_content.sbom_refs:
                self.sboms.append(self.load_sbom(sbom_ref))

            self.build_repository_search()

            for include in self.manifest_file_content.includes:
                local_path = None
                if include.local is not None:
                    local_path = (Path(self.manifest_location).parent / include.local).resolve()

                if (include.url or str(local_path)) in Manifest.loaded_manifests:
                    echo(
                        f"WARNING: Manifest file '{include.url or include.local}' "
                        "has already been loaded. Subsequent load requests ignored."
                    )

                    continue

                if include.url is not None:
                    self.children.append(Manifest.load_url(include.url, parent))

                if local_path is not None:
                    self.children.append(Manifest.load_file(local_path, parent))
