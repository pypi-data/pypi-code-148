"""
Manifest file data model
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, ClassVar, Generator, Literal

from hoppr_cyclonedx_models.cyclonedx_1_3 import CyclonedxSoftwareBillOfMaterialSpecification as Bom_1_3
from hoppr_cyclonedx_models.cyclonedx_1_4 import CyclonedxSoftwareBillOfMaterialsStandard as Bom_1_4
from pydantic import AnyUrl, Field, FileUrl, HttpUrl, NoneStr, create_model, validator
from pydantic.main import ModelMetaclass
from requests import HTTPError
from typer import secho

import hoppr.net
import hoppr.oci_artifacts
import hoppr.utils

from hoppr.exceptions import HopprLoadDataError
from hoppr.models.base import HopprBaseModel, HopprBaseSchemaModel
from hoppr.models.types import PurlType

if TYPE_CHECKING:
    from pydantic.typing import DictStrAny  # pragma: no cover


class Repository(HopprBaseModel):
    """
    Repository data model
    """

    url: HttpUrl | FileUrl
    description: NoneStr = None


# Dynamic Repositories model with PurlType values as attribute names
purl_type_repo_mapping = {str(purl_type): (list[Repository], Field([], unique_items=True)) for purl_type in PurlType}
Repositories: ModelMetaclass = create_model(  # type: ignore[call-overload]
    "Repositories", __base__=HopprBaseModel, **purl_type_repo_mapping
)


class LocalFile(HopprBaseModel):
    """
    LocalFile data model
    """

    local: Path


class OciFile(HopprBaseModel):
    """
    OciFile data model
    """

    oci: AnyUrl | str


class UrlFile(HopprBaseModel):
    """
    UrlFile data model
    """

    url: HttpUrl | FileUrl | AnyUrl | str


class Sbom(Bom_1_3, Bom_1_4):
    """
    Sbom data model that adds hash support
    """

    def __hash__(self) -> int:
        return hash(repr(self))


class IncludeRef(HopprBaseModel):
    """
    IncludeRef data model
    """

    __root__: LocalFile | UrlFile

    def __repr__(self) -> str:
        return repr(self.__root__)


class Includes(HopprBaseModel):
    """
    Data model for list of IncludeRef objects
    """

    __root__: list[IncludeRef]

    def __iter__(self) -> Generator[LocalFile | UrlFile, None, None]:  # type: ignore[override]
        for include_ref in self.__root__:
            yield include_ref.__root__

    def __getitem__(self, item):
        return self.__root__[item].__root__

    def __len__(self) -> int:
        return len(self.__root__)

    def __repr__(self) -> str:
        return f"Includes({repr(self.__root__)})"


class SbomRef(HopprBaseModel):
    """
    SbomRef data model
    """

    __root__: LocalFile | OciFile | UrlFile

    def __repr__(self) -> str:
        return repr(self.__root__)


class Sboms(HopprBaseModel):
    """
    Data model for list of SbomRef objects
    """

    __root__: list[SbomRef]

    def __iter__(self) -> Generator[LocalFile | OciFile | UrlFile, None, None]:  # type: ignore[override]
        for sbom_ref in self.__root__:
            yield sbom_ref.__root__

    def __getitem__(self, item):
        return self.__root__[item].__root__

    def __len__(self) -> int:
        return len(self.__root__)

    def __repr__(self) -> str:
        return f"Sboms({repr(self.__root__)})"


class ManifestFile(HopprBaseSchemaModel):
    """
    Data model to describe a single manifest file
    """

    kind: Literal["Manifest", "manifest"]
    includes: Includes = Field(Includes(__root__=[]), description="List of manifest files to load")
    repositories: Repositories = Field(  # type: ignore[valid-type]
        None, description="Maps supported PURL types to package repositories/registries"
    )
    sboms: Sboms = Field(Sboms(__root__=[]), description="List of SBOMs to process")

    # Attributes not included in schema
    loaded_manifests: ClassVar[set[LocalFile | UrlFile]] = set(Includes(__root__=[]))

    @validator("includes", allow_reuse=True)
    @classmethod
    def load_includes(cls, includes: Includes) -> list[ManifestFile]:
        """
        Validator that automatically loads manifest from local file or URL after initial parse
        """
        loaded_includes: list[ManifestFile] = []

        for include in includes:
            if include not in cls.loaded_manifests:
                cls.loaded_manifests.add(include)

                if isinstance(include, LocalFile):
                    loaded_includes.append(cls.parse_file(include.local))
                elif isinstance(include, UrlFile):
                    data = hoppr.net.load_url(include.url)
                    assert isinstance(data, dict), "URL manifest include was not loaded as dictionary"
                    loaded_includes.append(cls.parse_obj(data))

        return loaded_includes

    @classmethod
    def parse_file(cls, path: str | Path, *args, **kwargs) -> ManifestFile:  # pylint: disable=unused-argument
        """
        Override to resolve local file paths relative to manifest file
        """
        path = Path(path).resolve()

        data = hoppr.utils.load_file(path)
        if not isinstance(data, dict):
            raise TypeError("Local file content was not loaded as dictionary")

        # Resolve local file path references relative to manifest file path
        for sbom in data.get("sboms", []):
            if "local" in sbom:
                sbom["local"] = str((path.parent / sbom["local"]).resolve())

        for include in data.get("includes", []):
            if "local" in include:
                include["local"] = str((path.parent / include["local"]).resolve())

        return cls(**data)

    @classmethod
    def parse_obj(cls, obj: DictStrAny) -> ManifestFile:
        """
        Override to remove local file paths that can't be resolved
        """
        for include in list(obj.get("includes", [])):
            if "local" in include and not Path(include["local"]).is_absolute():
                secho(f"Skipping local include: relative path '{include['local']}' cannot be resolved", fg="yellow")
                obj["includes"].remove(include)

        for sbom in list(obj.get("sboms", [])):
            if "local" in sbom and not Path(sbom["local"]).is_absolute():
                secho(f"Skipping local SBOM: relative path '{sbom['local']}' cannot be resolved", fg="yellow")
                obj["sboms"].remove(sbom)

        return cls(**obj)


class Manifest(ManifestFile):
    """
    Manifest data model with SBOM references converted to Sbom objects in-place
    """

    # Redefine parent model fields as model types
    includes: list[ManifestFile] = Field(  # type: ignore[assignment]
        [],
        description="List of loaded manifest files",
        unique_items=True,
    )

    sboms: list[Sbom] = Field(  # type: ignore[assignment]
        [],
        description="List of loaded SBOM files",
        unique_items=True,
    )

    @validator("includes", allow_reuse=True, always=True, pre=True)
    @classmethod
    def load_includes(cls, includes: list[DictStrAny]) -> list[ManifestFile]:
        """
        Validator that automatically loads manifest from local file or URL after initial parse
        """
        loaded_includes: list[ManifestFile] = []

        for include in includes:
            include_obj = cls.parse_obj(include)
            loaded_includes.append(include_obj)

        return loaded_includes

    @validator("sboms", allow_reuse=True, always=True, pre=True)
    @classmethod
    def load_sboms(cls, sboms: list[DictStrAny]) -> list[Sbom]:
        """
        Validator that automatically loads SBOM from local file or URL
        """
        loaded_sboms: list[Sbom] = []

        for sbom in sboms:
            ref_type = list(sbom.keys())[0]
            match ref_type:
                case "local":
                    data = hoppr.utils.load_file(sbom["local"])
                    assert isinstance(data, dict), "Local file content was not loaded as dictionary"
                    loaded_sboms.append(Sbom(**data))
                case "oci":
                    data = hoppr.oci_artifacts.pull_artifact(sbom["oci"])
                    loaded_sboms.append(Sbom(**data))
                case "url":
                    data = hoppr.net.load_url(sbom["url"])
                    assert isinstance(data, dict), "URL SBOM file was not loaded as dictionary"
                    loaded_sboms.append(Sbom(**data))
                case _:
                    secho(f"Invalid SBOM reference: {ref_type} (must be one of: 'local', 'oci', 'url').", fg="yellow")

        return loaded_sboms

    @classmethod
    def load(cls, source: str | Path | DictStrAny) -> Manifest:
        """
        Load manifest from local file, URL, or dict
        """
        if isinstance(source, dict):
            data = ManifestFile.parse_obj(source).dict(by_alias=True)
        elif isinstance(source, Path):
            path = Path(source).resolve()
            manifest_file = ManifestFile.parse_file(path)
            data = cls._load_local_include(manifest_dir=path.parent, local_include=manifest_file)
        elif isinstance(source, str):
            try:
                include_dict = hoppr.net.load_url(source)
                if not isinstance(include_dict, dict):
                    raise TypeError("URL manifest include was not loaded as dictionary")

                manifest_file = ManifestFile.parse_obj(include_dict)
            except (HopprLoadDataError, HTTPError) as ex:
                raise HopprLoadDataError from ex

            data = cls._load_url_include(manifest_file)

        return cls(**data)

    @classmethod
    def _load_local_include(cls, manifest_dir: Path, local_include: ManifestFile) -> DictStrAny:
        for include in local_include.includes:
            if include is None or isinstance(include, Manifest):
                continue

            try:
                if isinstance(include, LocalFile):
                    include.local = (manifest_dir / include.local).resolve()
                    if include in cls.loaded_manifests:
                        raise HopprLoadDataError(include.local)

                    loaded = cls.load(Path(include.local))
                elif isinstance(include, UrlFile):
                    if include in cls.loaded_manifests:
                        raise HopprLoadDataError(include.url)

                    loaded = cls.load(str(include.url))
                else:
                    continue
            except HopprLoadDataError as ex:
                secho(f"Skipping previously loaded include: '{ex}'", fg="yellow")
                continue

            # Merge SBOMs, repositories, and includes from included manifest
            for purl_type in PurlType:
                repos = getattr(local_include.repositories, str(purl_type))
                add_repos = getattr(loaded.repositories, str(purl_type))
                repos.extend(add_repos)
                setattr(local_include.repositories, str(purl_type), list(set(repos)))

        return local_include.dict(by_alias=True)

    @classmethod
    def _load_url_include(cls, manifest_file: ManifestFile) -> DictStrAny:  # pylint: disable=too-many-branches
        for include in list(manifest_file.includes):
            try:
                if isinstance(include, LocalFile):
                    secho(f"Skipping local include: '{include.local}' cannot be resolved", fg="yellow")
                    manifest_file.includes.remove(include)  # type: ignore[attr-defined]
                    continue

                if isinstance(include, UrlFile):
                    if include in cls.loaded_manifests:
                        raise HopprLoadDataError(include.url)

                    include_dict = hoppr.net.load_url(include.url)
                    if not isinstance(include_dict, dict):
                        raise TypeError("URL manifest include was not loaded as dictionary")

                    # Recurse to populate additional manifest includes
                    loaded = cls.load(include_dict)

                    # Merge SBOMs, repositories, and includes from included manifest
                    for purl_type in PurlType:
                        repos = getattr(manifest_file.repositories, str(purl_type))
                        add_repos = getattr(loaded.repositories, str(purl_type))
                        repos.extend(add_repos)
                        setattr(manifest_file.repositories, str(purl_type), list(set(repos)))
                else:
                    continue
            except HopprLoadDataError as ex:
                secho(f"Skipping previously loaded include: '{ex}'", fg="yellow")
                continue
            except TypeError as ex:
                secho(str(ex), fg="red")
                continue

        return manifest_file.dict(by_alias=True)
