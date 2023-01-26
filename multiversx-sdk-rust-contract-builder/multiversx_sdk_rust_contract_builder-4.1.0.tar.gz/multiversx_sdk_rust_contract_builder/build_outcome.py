
import json
from pathlib import Path
from typing import Any, Dict

from multiversx_sdk_rust_contract_builder.cargo_toml import \
    get_contract_name_and_version
from multiversx_sdk_rust_contract_builder.filesystem import find_file_in_folder


class BuildOutcome:
    def __init__(self, context: str):
        self.context = context
        self.contracts: Dict[str, BuildOutcomeEntry] = dict()

    def gather_artifacts(self, contract_name: str, build_folder: Path, output_subfolder: Path):
        self.contracts[contract_name] = BuildOutcomeEntry.from_folders(build_folder, output_subfolder)

    def get_entry(self, contract_name: str) -> 'BuildOutcomeEntry':
        return self.contracts[contract_name]

    def save_to_file(self, file: Path):
        data = self.to_dict()

        with open(file, "w") as f:
            json.dump(data, f, indent=4)

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"context": self.context}

        for key, value in self.contracts.items():
            data[key] = value.to_dict()

        return data


class BuildOutcomeEntry:
    def __init__(self) -> None:
        self.version = ""
        self.codehash = ""
        self.build_path = ""
        self.artifacts = BunchOfBuildArtifacts()

    @classmethod
    def from_folders(cls, build_folder: Path, output_folder: Path) -> 'BuildOutcomeEntry':
        entry = BuildOutcomeEntry()
        _, entry.version = get_contract_name_and_version(build_folder)
        entry.codehash = find_file_in_folder(output_folder, "*.codehash.txt").read_text()
        entry.artifacts = BunchOfBuildArtifacts.from_output_folder(output_folder)
        return entry

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "codehash": self.codehash,
            "buildPath": self.build_path,
            "artifacts": self.artifacts.to_dict()
        }


class BunchOfBuildArtifacts:
    def __init__(self) -> None:
        self.bytecode = BuildArtifact(Path(""))
        self.text = BuildArtifact(Path(""))
        self.abi = BuildArtifact(Path(""))
        self.imports = BuildArtifact(Path(""))
        self.src_package = BuildArtifact(Path(""))
        self.output_archive = BuildArtifact(Path(""))

    @classmethod
    def from_output_folder(cls, output_folder: Path) -> 'BunchOfBuildArtifacts':
        artifacts = BunchOfBuildArtifacts()
        artifacts.bytecode = BuildArtifact.find_in_output("*.wasm", output_folder)
        artifacts.text = BuildArtifact.find_in_output("*.wat", output_folder)
        artifacts.abi = BuildArtifact.find_in_output("*.abi.json", output_folder)
        artifacts.imports = BuildArtifact.find_in_output("*.imports.json", output_folder)
        artifacts.src_package = BuildArtifact.find_in_output("*.source.json", output_folder)

        return artifacts

    def to_dict(self) -> Dict[str, str]:
        return {
            "bytecode": self.bytecode.path.name,
            "text": self.text.path.name,
            "abi": self.abi.path.name,
            "imports": self.imports.path.name,
            "srcPackage": self.src_package.path.name,
            "outputArchive": self.output_archive.path.name
        }


class BuildArtifact:
    def __init__(self, path: Path) -> None:
        self.path = path

    @classmethod
    def find_in_output(cls, name_pattern: str, output_folder: Path) -> 'BuildArtifact':
        path = find_file_in_folder(output_folder, name_pattern)
        return BuildArtifact(path)

    def read(self) -> bytes:
        with open(self.path, "rb") as f:
            return f.read()
